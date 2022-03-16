from pathlib import Path

from numpy import timedelta64
from pandas import read_csv, DataFrame, to_datetime

project_folder = r'/gpfs2/scratch/tcbarret/completed_downloader_runs/all_states_20220207_0_to_18_months'
# project_folder = r'/gpfs2/scratch/tcbarret/completed_downloader_runs/all_states_20220315_18_to_30_months'
# project_folder = r'E:\USGS_Downloader\test_slurm_runs\debug_set'
output_folder = r'/gpfs2/scratch/tcbarret/completed_downloader_runs'
# output_folder = r'E:\USGS_Downloader\test_slurm_runs'

project_path = Path(project_folder)
project_name = project_path.parts[-1]
output_path = Path(output_folder)

report_files = sorted(project_path.rglob('*.csv'))
laz_files = sorted(project_path.rglob('*.laz'))
laz_df = DataFrame({'filepath': laz_files})
laz_df['ClipFileSize'] = laz_df['filepath'].apply(lambda x: x.stat().st_size)
laz_df['ClipFile'] = laz_df['filepath'].apply(lambda x: x.name)

combined_df = DataFrame()
for report_file in report_files:
    filename = report_file.name
    print(f'Processing {filename}')
    state = filename[:2]
    state_df = read_csv(report_file)
    state_df.insert(0, 'State', state)
    print(state_df.head())
    combined_df = combined_df.append(state_df)

combined_df = combined_df.merge(laz_df, how='left', on='ClipFile')
combined_df['ClipFileSizeCat'] = ''
combined_df.loc[combined_df['ClipFileSize'].isna(), 'ClipFileSizeCat'] = 'NoFile'
combined_df.loc[combined_df['ClipFileSize'] < 0.1, 'ClipFileSizeCat'] = 'EmptyFile'
combined_df.loc[(combined_df['ClipFileSize'] > 0.1) & (combined_df['ClipFileSize'] <= 1000),
                'ClipFileSizeCat'] = 'SmallFile'
combined_df.loc[combined_df['ClipFileSize'] > 1000, 'ClipFileSizeCat'] = 'CandidateFile'

combined_df['MonthDelta'] = (to_datetime(combined_df['avedate'])
                             - to_datetime(combined_df['measdate'])).apply(abs) \
                            / timedelta64(1, 'M')

print(f'Total records: {len(combined_df)}')
print(f'Categories: \n{combined_df["ClipFileSizeCat"].value_counts()}')

combined_df.drop(columns=['filepath']).sort_values(['State', 'CN']).to_csv(
    output_path / f'{project_name}.csv', index=False)
