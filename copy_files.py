from pathlib import Path

from shutil import copy2

input_folder = '/gpfs2/scratch/tcbarret/completed_downloader_runs/noaa_retrievals_20220628'
output_folder = '/gpfs2/scratch/tcbarret/completed_dataprep_runs/quality_check_20220629_noaa_as_downloaded__reporting/05_problem_laz_files'
copy_only_first_match = False  # Faster, but doesn't ensure uniqueness
keyword_list = [
    '522_236617012010854',
    '522_236617176010854',
    '522_249673342010854',
    '522_249673383010854',
    '522_259177984010854',
    '522_259085016010854',
    '522_259085032010854',
    '540_153666060010854',
    '540_174758516020004',
    '540_174758537020004',
    '540_228183329010854',
    '540_259084971010854',
    '531_221353737010661',
    '531_247057117010661',
    '522_249676358010854',
    '540_197125538010854',
    '540_259118863010854',
    '521_168988973010661',
    '521_222442739010661',
    '521_247063050010661',
    '521_247063054010661',
    '1061_47885274020004',
    '531_155531778010854',
    '531_155531785010854',
    '531_252281777010854',
]

input_path = Path(input_folder)
output_path = Path(output_folder)
output_path.mkdir()

input_files = sorted(input_path.rglob('*'))

for keyword in keyword_list:
    print(f'Keyword: {keyword}')
    for input_file in input_files:
        if keyword in str(input_file):
            print(f'Copying: {input_file.name}')
            copy2(input_file, output_path)
            if copy_only_first_match:
                break
