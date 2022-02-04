#!/bin/bash

### Slurm header section ###

# Job name
#SBATCH --job-name=downloader_step_1

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
#SBATCH --cpus-per-task=4

# Memory (default is 1G, for entire job, can specify by entire job or by core)

# Email
#SBATCH --mail-type=ALL

# Rename log file to "<myjob>_<jobid>.out" -- Not working this way, so implemented differently, below
# #SBATCH –-output=%x_%j.out

### Executable section ###

# Echo each command to the log file
set -x

cd "$HOME/code/run_usgs_downloader"

# Link log file to one with a preferred name, and in the output folder - TODO: Fix linking to scratch drive
#ln -f "$HOME/code/run_usgs_downloader/slurm-$SLURM_JOB_ID.out" "/gpfs2/scratch/tcbarret/downloader/${SLURM_JOB_NAME}_$SLURM_JOB_ID.out"
ln -f "slurm-$SLURM_JOB_ID.out" "${SLURM_JOB_NAME}_$SLURM_JOB_ID.out"

~/miniconda3/condabin/conda run --prefix ~/miniconda3/envs/usgs_downloader bash batch_step_1_eastern_states.sh