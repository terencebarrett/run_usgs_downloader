USGS Downloader
===============

Downloads USGS LiDAR coverage of FIA plots with the packages `USGSlidar` (R) 
and `pdal` (Python) from a single combined R/Python conda environment. 

The code in this repo is currently only intended for exploring these tools' 
capabilities and for investigating possibilities for productionizing their use.

The `USGSlidar` package used is a fork, modified to run on Linux, of a package 
developed for Windows by Robert J. McGaughey (GitHub: bmcgaughey1). The plan is to 
ensure that this fork works equally well for both OS, and then open a PR for the 
Linux support to be incorporated in the original package.

Tested on Linux - Ubuntu 20 and RedHat Enterprise 7

Start here if setting up to run in a RedHat VM, otherwise skip to the next section
----------------------------------------------------------------------------------
1. Clone this repo to the host machine
2. Install Vagrant and Virtual Box on the host machine
3. (host) `cd` to root of repo
4. (host) Review the `memory` and `cpus` settings in the file `Vagrantfile`; edit if necessary
5. (host) `vagrant up` to build the VM, based on the configuration in the `Vagrantfile`
6. (host) `vagrant ssh` to enter the VM
7. (vm) `cd /vagrant` to be at the root of the code base (this folder is shared with the host)
8. (vm) `./setup_vm.sh` to install Miniconda
   - Accept all defaults, apart from replying `yes` to the running of "conda init"
9. (vm) `exit` (Need to re-enter the vm so `conda` will be available)
10. (host) `vagrant ssh` to re-enter the VM
11. (vm) `cd /vagrant` to be at the root of the code base
12. (vm) Continue setup with step (4) in the next section

Setting up USGS Downloader  
--------------------------
- Creates a single combined Python/R conda environment used for all steps of the workflow

1. Clone this repo
2. Install `Miniconda` (preferred) or `Anaconda`, if neither of these are currently installed
3. `cd` to root of repo
4. `$ conda config --set channel_priority strict`
5. `$ conda env create -f conda_linux.yaml`
6. `$ conda activate usgs_downloader`
7. `(usgs_downloader) $ Rscript setup_step_1.R`
   - Note: *ggspatial* does not yet have a conda package - that is why it is installed by this script 
   and not via conda, the preferred way; see https://githubmemory.com/repo/paleolimbot/ggspatial/issues/83
8. `(usgs_downloader) $ Rscript setup_step_2.R`
   - This is also the script to run later on to upgrade the USGSlidar dependency 
   
Running USGS Downloader for the example provided - the state of Delaware
------------------------------------------------------------------------
1. `$ conda activate usgs_downloader`
2. `cd` to root of repo
3. Delete the contents of the repo’s *working* folder (the results of the previous run) -- if want to 
start fresh
4. `(usgs_downloader) $ Rscript run_step_1.R`
   - Expected output to the *working* folder:
     - DEPlots.csv
     - ENTWINEBoundaries.gpkg
     - FIADB_DE.db
   - Expected output to the *working/DE/pipelines* folder:
     - RUNME.bat, a batch file listing the pdal-pipeline commands
     - A number of pdal-pipeline *json* files
5. `(usgs_downloader) $ python run_step_2.py`
   - Expected output to the *working/DE/clips* folder:
     - A number of *laz* files, one for each *json* file
     - The *laz* point clouds should be a number of small point cloud tiles scattered throughout 
     the state of Delaware







