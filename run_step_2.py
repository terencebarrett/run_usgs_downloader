from pathlib import Path
from subprocess import run

# TODO: Multiprocess the commands
# TODO: Make the input parameters into CLI args

# Input parameter
state = 'DE'
pipelines = 'pipelines'
bat_file = 'RUNME.bat'

# Read pdal-pipeline commands
runtime_path = Path(__file__).parent
working_path = runtime_path / 'working' / state / pipelines
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

