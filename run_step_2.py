from argparse import ArgumentParser
from json import load
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from os import name
from pathlib import Path
from shlex import split
from subprocess import run, Popen, PIPE
from timeit import default_timer as timer

from numpy import around


# TODO: Make all input parameters into CLI args
# TODO: Report with download result (sizable file, 1kb file, no file, error messages


# Read CLI arguments
parser = ArgumentParser()
parser.add_argument('-s', '--state', type=str, default='DE',
                    help="2-letter state abbreviation")
parser.add_argument('-c', '--cores', type=int, default=None,
                    help="Number of parallel processes, or None to use cpu_count() - 1")
args = parser.parse_args()


# Input and echo parameters
repo_working_folder = False  # `True` to use the repo's `working` folder as the working folder
outside_working_folder_path = '/gpfs2/scratch/tcbarret/downloader'  # Only needed if repo_working_folder is `False`; folder must exist
state = args.state
pipelines = 'pipelines'
bat_file = 'RUNME.bat'
multiprocess = True  # If `True`, will multiprocess with one less than the total available cores
user_cores = args.cores

print(f'Processing state: {state}')

# Read pdal-pipeline commands
start_timing = timer()
if repo_working_folder:
    runtime_path = Path(__file__).parent
    working_path = runtime_path / 'working' / state / pipelines
else:
    working_path = Path(outside_working_folder_path) / state / pipelines

with open(working_path / bat_file) as f:
    command_lines_raw = f.readlines()
command_lines = command_lines_raw[1:]  # Skip comment in first line of the (Windows) batch file
num_pipelines = len(command_lines)

pipeline_dict = {Path(command.strip().split()[2]).stem.split('_')[-1]:
                    {'command': command.strip(),
                     'pipeline_filepath': Path(command.strip().split()[2])}
                 for command in command_lines}

result_dict = pipeline_dict.copy()
for id, id_dict in pipeline_dict.items():
    with open(str(id_dict['pipeline_filepath'])) as f:
        json_dict = load(f)
        output_filepath = Path(json_dict[1]['filename'])
        result_dict[id]['output_filepath'] = output_filepath


def file_sizes(input_dict):
    output_dict = input_dict.copy()
    for id, id_dict in input_dict.items():
        output_filepath = id_dict['output_filepath']
        output_dict[id]['output_size'] = output_filepath.stat().st_size \
            if output_filepath.exists() else 0
    total_size = sum([size for size in [one_id_dict['output_size']
                                        for one_id_dict in output_dict.values()]])
    cmds_zero_size = [one_id_dict['command'] for one_id_dict in output_dict.values()
                      if one_id_dict['output_size'] == 0]
    return output_dict, total_size, cmds_zero_size


result_dict, start_size, commands = file_sizes(result_dict)
if start_size > 0:
    raise RuntimeError('Clear output folder and restart')
num_pipelines = len(commands)
print(f'Processing {num_pipelines} PDAL pipelines')

# Run PDAL pipelines
if multiprocess:
    def call_process(cmd):
        posix = name == 'posix'
        p = Popen(split(cmd, posix=posix),
                  stdout=PIPE,
                  stderr=PIPE,
                  universal_newlines=True)
        stdout, stderr = p.communicate()
        return stdout, stderr

    cpu_count = cpu_count()
    cores = user_cores if user_cores else str(cpu_count - 1)
    print(f'Running on {cores} cores of the {cpu_count} available')
    pool = ThreadPool(int(cores))
    results = []
    for command in commands:
        results.append(pool.apply_async(call_process, [command]))

    # Close the pool and wait for each running task to complete
    pool.close()
    pool.join()

    # Report messages from all processes
    for result in results:
        process_out, process_error = result.get()
        if process_out:
            print('Communication from the process on the stdout pipe:\n', process_out)
        if process_error:
            print('Communication from the process on the stderr pipe:\n', process_error)

else:
    # Execute pdal-pipeline commands one at a time
    print(f'Running on one core')
    for command in commands:
        print(f'Running command: {command}')
        command_args = command.split()
        result = run(command_args,
                     capture_output=True,
                     cwd=working_path,
                     universal_newlines=True)
        print(f'stdout: \n{result.stdout}') if result.stdout else None
        print(f'stderr: \n{result.stderr}') if result.stderr else None

# Get size of downloaded files
result_dict, downloaded_size, retry_commands = file_sizes(result_dict)
print(f'Total size downloaded: {downloaded_size} bytes')

if retry_commands:
    print(f'{len(retry_commands)} downloads failed')
    print('Retrying pdal-pipeline commands that failed, one at a time')
    for command in retry_commands:
        print(f'Running command: {command}')
        command_args = command.split()
        result = run(command_args,
                     capture_output=True,
                     cwd=working_path,
                     universal_newlines=True)
        print(f'stdout: \n{result.stdout}') if result.stdout else None
        print(f'stderr: \n{result.stderr}') if result.stderr else None

    # Get size of downloaded files
    result_dict, downloaded_size, failed_commands = file_sizes(result_dict)

    print(f'Total size downloaded: {downloaded_size} bytes')
    if failed_commands:
        print(f'{len(failed_commands)} downloads failed')

stop_timing = timer()
process_time_minutes = (stop_timing - start_timing) / 60
print('\nTotal processing time: {} minutes'.format(around(process_time_minutes, 1)))
