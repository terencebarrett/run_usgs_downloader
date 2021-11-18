#!/bin/bash

### Slurm header section ###

# Job name
#SBATCH --job-name=logfile

# Partition
# `short`: jobs < 3 hrs; `bluemoon`/`bigmem` < 30 hrs; `week`/`bigmemwk`: < 7 days
#SBATCH --partition=short

# Walltime (hh:mm:ss)
# End job if hits this to not run afoul of partition guideline
#SBATCH --time=03:00:00

# Nodes
#SBATCH --nodes=1

# Processes/Tasks per Node
#SBATCH --ntasks=1

# Cores per Process/Task
#SBATCH --cpus-per-task=1

# Memory (default is 1G, for entire job, can specify by entire job or by core)

# Email
#SBATCH --mail-type=ALL

# Rename log file to "<myjob>_<jobid>.out"
# #SBATCH –-output=%x_%j.out

### Executable section ###

# Echo each command to the log file
set -x

cd ${HOME}

# Link log file to one with a preferred name
ln -f ~/code/run_usgs_downloader/slurm-$SLURM_JOB_ID.out ~/code/run_usgs_downloader/working/DE/$SLURM_JOB_NAME_$SLURM_JOB_ID.out

echo "Test for log file renaming and copying"
env
