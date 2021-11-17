#!/bin/bash

### Slurm header section ###

# Job name
#SBATCH --job-name=downloader

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
#SBATCH --cpus-per-task=16

# Memory (default is 1G, for entire job, can specify by entire job or by core)

# Email
#SBATCH --mail-type=ALL

# Rename log file to "<myjob>_<jobid>.out"
# #SBATCH –-output=%x_%j.out

### Executable section ###

# Echo each command to the log file
set -x

cd ${HOME}
~/miniconda3/condabin/conda run --prefix ~/miniconda3/envs/usgs_downloader python ~/code/run_usgs_downloader/run_step_2.py -s DE -c 127

# Copy log file to results folder