from pathlib import Path
from subprocess import run

# TODO: Multiprocess the commands

# Input parameter
# Note: The leading `\` of the file name is likely an artifact of running the
# Windows-developed `USGSlidar` on Linux; modify the name to match the file
# produced in Step 1, if different than below.
# TODO: Make this into a CLI arg
bat_file = r'\RUNME.bat'

# Read pdal-pipeline commands
runtime_path = Path(__file__).parent
working_path = runtime_path / 'working'
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

