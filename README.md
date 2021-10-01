USGS Downloader
===============

Download USGS LiDAR coverage of FIA plots with the packages `USGSlidar` (R) 
and `pdal` (Python) from a single combined R/Python conda environment. 

The code in this repo is currently only intended for exploring these tools' 
capabilities and for investigating possibilities for productionizing their use.

Tested on Linux (Ubuntu 20), but should be OS-agnostic.

Setting up USGS Downloader  
--------------------------
- Creates a single combined Python/R conda environment used for all steps of the workflow

1. Clone this repo
2. `cd` to root of repo
3. `$ conda env create -f conda.yaml`
4. `$ conda activate usgs_downloader`
5. `(usgs_downloader) $ Rscript setup.R`
   - Note: *ggspatial* does not yet have a conda package - that is why it is installed by this script 
   and not via conda, the preferred way; see https://githubmemory.com/repo/paleolimbot/ggspatial/issues/83


Running USGS Downloader for the example provided - the state of Delaware
------------------------------------------------------------------------
1. `$ conda activate usgs_downloader`
2. `cd` to root of repo
3. Delete the contents of the repo’s *working* folder (the results of the previous run) -- if want to start fresh
4. `(usgs_downloader) $ Rscript run_step_1.R`
   - Expected output (to the *working* folder of the repo):
     - DEPlots.csv
     - ENTWINEBoundaries.gpkg
     - FIADB_DE.db
     - RUNME.bat, a batch file listing the pdal-pipeline commands
     - A number of pdal-pipeline *json* files
5. `(usgs_downloader) $ python run_step_2.py`
   - Expected output (to the *working* folder of the repo):
     - A number of *laz* files, one for each *json* file
     - The *laz* point clouds should be a number of small point cloud tiles scattered throughout the state of Delaware







