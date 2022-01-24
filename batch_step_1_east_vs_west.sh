#!/bin/bash

Rscript "$HOME/code/run_usgs_downloader/run_step_1.R" -s DE -c 1000
Rscript "$HOME/code/run_usgs_downloader/run_step_1.R" -s CO -c 1000 --local_entwine_index
