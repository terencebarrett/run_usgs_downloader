from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from os import name
from pathlib import Path
from shlex import split
from subprocess import run, Popen, PIPE
from timeit import default_timer as timer

from numpy import around


# TODO: Make the input parameters into CLI args


# Input parameters
repo_working_folder = True  # `True` to use the repo's `working` folder as the working folder
outside_working_folder_path = '/vagrant/Odrive/Tools/PythonScripts/Terry/USGS_Downloader/test_VM_to_O'  # Only needed if repo_working_folder is `False`; folder must exist
state = 'DE'
pipelines = 'pipelines'
bat_file = 'RUNME.bat'
multiprocess = False  # If `True`, will multiprocess with one less than the total available cores


# Read pdal-pipeline commands
start_timing = timer()
if repo_working_folder:
    runtime_path = Path(__file__).parent
    working_path = runtime_path / 'working' / state / pipelines
else:
    working_path = Path(outside_working_folder_path) / state / pipelines

with open(working_path / bat_file) as f:
    commands_raw = f.readlines()
commands = commands_raw[1:]  # Skip comment in first line of the (Windows) batch file

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

    cores = str(cpu_count() - 1)
    print(f'Running on {cores} cores')
    pool = ThreadPool(int(cores))
    results = []
    for command in commands:
        command_stripped = command.strip()
        results.append(pool.apply_async(call_process, [command_stripped]))

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
        command_stripped = command.strip()
        print(f'Running command: {command_stripped}')
        command_args = command_stripped.split()
        result = run(command_args,
                     capture_output=True,
                     cwd=working_path,
                     universal_newlines=True)
        print(f'stdout: \n{result.stdout}') if result.stdout else None
        print(f'stderr: \n{result.stderr}') if result.stderr else None

stop_timing = timer()
process_time_minutes = (stop_timing - start_timing) / 60
print('\nTotal processing time: {} minutes'.format(around(process_time_minutes, 1)))
