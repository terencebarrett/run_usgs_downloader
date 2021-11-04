from pathlib import Path
from subprocess import run

# TODO: Multiprocess the commands
# TODO: Make the input parameters into CLI args

# Input parameters
repo_working_folder = True  # `True` to use the repo's `working` folder as the working folder
outside_working_folder_path = '/vagrant/Odrive/Tools/PythonScripts/Terry/USGS_Downloader/test_VM_to_O'  # Only needed if repo_working_folder is `False`; folder must exist
state = 'DE'
pipelines = 'pipelines'
bat_file = 'RUNME.bat'

# Read pdal-pipeline commands
if repo_working_folder:
    runtime_path = Path(__file__).parent
    working_path = runtime_path / 'working' / state / pipelines
else:
    working_path = Path(outside_working_folder_path) / state / pipelines

with open(working_path / bat_file) as f:
    commands = f.readlines()

# Execute pdal-pipeline commands
for command in commands[1:]:  # Skip comment in first line of (Windows) batch file
    command_stripped = command.strip()
    print(f'Running command: {command_stripped}')
    command_args = command_stripped.split()
    result = run(command_args,
                 capture_output=True,
                 cwd=working_path,
                 universal_newlines=True)
    print(f'stdout: \n{result.stdout}') if result.stdout else None
    print(f'stderr: \n{result.stderr}') if result.stderr else None

