from spikeinterface_gui import run_mainwindow
import spikeinterface.full as si
import json
import numpy as np

using_real_data = False

if using_real_data:
    analyzer = si.load_sorting_analyzer('/home/nolanlab/Desktop/sub-03_day-06_ses-OF1_srt-kilosort4A_analyzer.zarr')
else:
    si.set_global_job_kwargs(n_jobs=4)
    print("\nCreating artificial recording and sorting, and computing properties...\n")
    recording, sorting = si.generate_ground_truth_recording(num_channels=96, num_units=96*2, durations=[60*30])
    analyzer = si.create_sorting_analyzer(sorting, recording, peak_sign='both')
    analyzer.compute(['random_spikes', 'noise_levels', 'waveforms', 'templates', 'spike_amplitudes', 'correlograms', 'template_metrics', 'unit_locations', 'principal_components'])
    analyzer.compute('quality_metrics', metric_names=['snr'])

print("\nLaunching GUI...\n")

layout = 'fig4/merge_layout.json'
settings_file = 'fig4/merge_settings.json'
with open(settings_file, "r") as f:
    user_settings = json.load(f)

extra_unit_properties = {
    'brain_area': np.array(['ENT', 'VIS']*1000)[:len(analyzer.unit_ids)]
}

run_mainwindow(
    analyzer,
    layout = 'fig4/merge_layout.json',
    user_settings=user_settings,
    curation=True,
    extra_unit_properties = extra_unit_properties,
    mode='desktop',
)
