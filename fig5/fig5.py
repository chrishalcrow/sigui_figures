from pathlib import Path

from spikeinterface_gui import run_mainwindow
import spikeinterface.full as si
import pandas as pd

import pynapple as nap
import numpy as np

def main():
    
    use_real_data = False
    
    if use_real_data:
        
        active_projects_folder = Path('/run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/')
        
        position_df = pd.read_pickle(active_projects_folder / "Bri/optetrode_recordings/chR2/1544/1544_2023-05-05_11-30-05_opto/MountainSort/DataFrames/position.pkl")
        position = nap.TsdFrame(position_df['synced_time'].values, np.transpose(np.array([position_df['position_x'].values, position_df['position_y'].values])), columns=["x", "y"])
        
        analyzer = si.load_sorting_analyzer('sub-1544_ses-2023-05-05-05opto_analyzer')
        pp_rec = analyzer._recording
        
        opto_path = active_projects_folder / 'Bri/optetrode_recordings/chR2/1544/1544_2023-05-05_11-30-05_opto/MountainSort/DataFrames/opto_pulses.pkl'
        opto_pulses = pd.read_pickle(opto_path)
    
    else:
    
        start_frame = 0
        end_frame = 30_000*60
    
        opto_start_times = np.arange(start_frame, end_frame, 40_000)
        opto_end_times = opto_start_times + 90
        opto_pulses = pd.DataFrame(columns=['opto_start_times', 'opto_end_times'], data=np.transpose(np.vstack([opto_start_times, opto_end_times])))
    
        position_array = generate_path(end_frame//30_000)
        position_timeseries = np.arange(start_frame, end_frame, 1000)/30_000
    
        position = nap.TsdFrame(t=position_timeseries, d=position_array, columns=['x','y'])
    
        si.set_global_job_kwargs(n_jobs=4)
        print("\nCreating artificial recording and sorting, and computing properties...\n")
        recording, sorting = si.generate_ground_truth_recording(num_channels=4, num_units=7, durations=[end_frame/30_000], seed=1205)
        analyzer = si.create_sorting_analyzer(sorting, recording, peak_sign='both')
        analyzer.compute(['random_spikes', 'noise_levels', 'waveforms', 'templates', 'spike_locations', 'correlograms', 'quality_metrics', 'template_metrics', 'unit_locations'])
    
    events = {
        'start': {
            'samples': opto_pulses['opto_start_times'].values,
        },
        'stop': {
            'samples': opto_pulses['opto_end_times'].values,
        },
    }
    
    
    bri_layout = dict(
        zone1=['ratemapview'],
        zone2=[],
        zone3=['unitlist'],
        zone4=['trace'],
        zone5=['event'],
        zone6=[],
        zone7=['spikelist'],
        zone8=['waveform'],
    )
    
    user_settings = {
        "waveform": {
            "overlap": False,
            "plot_selected_spike": True,
            "plot_waveforms_samples": False,
            "y_scalebar": True,
        },
        "spikeamplitude": {
            "max_spikes_per_unit": 10000,
        },
        "spikerate": {
            "bin_s": 30
        },
        "events": {
            "max_trials": 1000,
        }
    }
    
    run_mainwindow(
        analyzer,
        mode="desktop",
        curation=True,
        verbose=True,
        layout=bri_layout,
        user_settings=user_settings,
        recording=None,
        external_data={'position': position},
        events=events,
    )
    

def generate_path(duration_sec, area_size=100, avg_speed=2.0):
    """
    Generates a random continuous path. Created by Gemini.
    """
    # 1. Setup parameters
    # We'll treat each index as 1 second to match your 1cm/s speed requirement
    t = np.arange(0, duration_sec, 1/30)
    path = np.zeros((30*duration_sec, 2))
    
    # Start in the center
    path[0] = [area_size / 2, area_size / 2]
    
    # 2. Generate movement
    # We use a smoothed random walk (Brownian motion style)
    # Volatility determines how much the 'direction' changes
    volatility = 0.8 
    
    # Initialize velocity
    v = np.array([avg_speed, 0.0]) 
    
    for i in range(1, 30*duration_sec):
        # Add random noise to velocity
        angle = np.random.uniform(-volatility, volatility)
        c, s = np.cos(angle), np.sin(angle)
        rotation_matrix = np.array(((c, -s), (s, c)))
        
        # Rotate the velocity vector and normalize to avg_speed
        v = rotation_matrix @ v
        
        # Calculate next position
        next_pos = path[i-1] + v
        
        # 3. Boundary Control (Bounce back if hitting walls)
        for dim in range(2):
            if next_pos[dim] < 0 or next_pos[dim] > area_size:
                v[dim] *= -1  # Reflect velocity
                next_pos[dim] = path[i-1][dim] + v[dim]
        
        path[i] = next_pos
        
    return path

if __name__ == '__main__':
    main()
