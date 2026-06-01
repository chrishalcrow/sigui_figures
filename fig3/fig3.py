from spikeinterface_gui import run_mainwindow
import spikeinterface.full as si
import json

using_real_data = False

if using_real_data:
    analyzer = si.load_sorting_analyzer('/run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Wolf/MMNAV/derivatives/M05/D04/MMNAV1/kilosort4A/sub-05_day-04_ses-MMNAV1_srt-kilosort4A_analyzer.zarr')
    recording = si.read_openephys(
        '/run/user/1000/gvfs/smb-share:server=cmvm.datastore.ed.ac.uk,share=cmvm/sbms/groups/CDBS_SIDB_storage/NolanLab/ActiveProjects/Wolf/MMNAV/raw/VR/M05_D04_2025-11-16_14-46-40_MMNAV1/Record Node 109'
    )
else:
    si.set_global_job_kwargs(n_jobs=4)
    print("\nCreating artificial recording and sorting, and computing properties...\n")
    recording, sorting = si.generate_ground_truth_recording(num_channels=96, num_units=96*2, durations=[60*1], seed=1205)
    analyzer = si.create_sorting_analyzer(sorting, recording, peak_sign='both')
    analyzer.compute(['random_spikes', 'noise_levels', 'waveforms', 'templates', 'spike_locations', 'correlograms', 'quality_metrics', 'template_metrics', 'unit_locations'])

print("\nLaunching GUI...\n")

pp_recording = si.common_reference(si.bandpass_filter(recording))

settings_file = 'fig3/spike_settings.json'
with open(settings_file, "r") as f:
    user_settings = json.load(f)

run_mainwindow(
    analyzer,
    recording = pp_recording,
    layout = 'fig3/spike_layout.json',
    user_settings=user_settings,
)
