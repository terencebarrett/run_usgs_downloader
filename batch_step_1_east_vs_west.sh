#!/bin/bash

Rscript run_step_1.R -s DE -c 1000
Rscript run_step_1.R -s CO -c 1000 --local_entwine_index
