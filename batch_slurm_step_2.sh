#!/bin/bash

sbatch --dependency=singleton slurm_step_2.sh DE
sbatch --dependency=singleton slurm_step_2.sh VT
