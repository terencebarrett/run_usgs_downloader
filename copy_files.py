from pathlib import Path

from shutil import copy2

input_folder = '/gpfs2/scratch/tcbarret/zip_processing/Park/2019/Products/LAS'
output_folder = '/gpfs2/scratch/tcbarret/zip_processing/Park_selection'
keyword_list = ['CWCB_PARK_04331',
                'CWCB_PARK_04332',
                'CWCB_PARK_04333',
                'CWCB_PARK_04334',
                'CWCB_PARK_04335',
                'CWCB_PARK_04385',
                'CWCB_PARK_04386',
                'CWCB_PARK_04387',
                'CWCB_PARK_04388',
                'CWCB_PARK_04389',
                'CWCB_PARK_04439',
                'CWCB_PARK_04440',
                'CWCB_PARK_04492',
                'CWCB_PARK_04493',
                'CWCB_PARK_04543',
                'CWCB_PARK_04544',
                'CWCB_PARK_04594',
                'CWCB_PARK_04595',
                'CWCB_PARK_04645',
                'CWCB_PARK_04646',
                'CWCB_PARK_04696',
                'CWCB_PARK_04697',
                'CWCB_PARK_04747',
                'CWCB_PARK_04748',
                'CWCB_PARK_04797',
                'CWCB_PARK_04798',
                'CWCB_PARK_04847',
                'CWCB_PARK_04848',
                'CWCB_PARK_04898',
                'CWCB_PARK_04899',
                'CWCB_PARK_04950',
                'CWCB_PARK_04951',
                'CWCB_PARK_05002',
                'CWCB_PARK_05003',
                'CWCB_PARK_05054',
                'CWCB_PARK_05055',
                'CWCB_PARK_05106',
                'CWCB_PARK_05107',
                'CWCB_PARK_05156',
                'CWCB_PARK_05157',
                'CWCB_PARK_05204',
                'CWCB_PARK_05205',
                'CWCB_PARK_05253',
                'CWCB_PARK_05254']

input_path = Path(input_folder)
output_path = Path(output_folder)
output_path.mkdir()

input_files = sorted(input_path.glob('*'))

for keyword in keyword_list:
    print(f'Keyword: {keyword}')
    for input_file in input_files:
        if keyword in str(input_file):
            print(f'Copying: {input_file.name}')
            copy2(input_file, output_path)
            break


