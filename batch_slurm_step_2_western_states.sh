#!/bin/bash

sbatch --dependency=singleton slurm_step_2.sh AK
sbatch --dependency=singleton slurm_step_2.sh AS
sbatch --dependency=singleton slurm_step_2.sh AZ
sbatch --dependency=singleton slurm_step_2.sh CA
sbatch --dependency=singleton slurm_step_2.sh CO
sbatch --dependency=singleton slurm_step_2.sh GU
sbatch --dependency=singleton slurm_step_2.sh HI
sbatch --dependency=singleton slurm_step_2.sh ID
sbatch --dependency=singleton slurm_step_2.sh KS
sbatch --dependency=singleton slurm_step_2.sh MP
sbatch --dependency=singleton slurm_step_2.sh MT
sbatch --dependency=singleton slurm_step_2.sh ND
sbatch --dependency=singleton slurm_step_2.sh NE
sbatch --dependency=singleton slurm_step_2.sh NM
sbatch --dependency=singleton slurm_step_2.sh NV
sbatch --dependency=singleton slurm_step_2.sh OK
sbatch --dependency=singleton slurm_step_2.sh OR
sbatch --dependency=singleton slurm_step_2.sh SD
sbatch --dependency=singleton slurm_step_2.sh TX
sbatch --dependency=singleton slurm_step_2.sh UT
sbatch --dependency=singleton slurm_step_2.sh WA
sbatch --dependency=singleton slurm_step_2.sh WY
