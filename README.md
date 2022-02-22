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

Set up on the VACC
------------------
- Log in to a VACC node: `ssh <NetID>@<vacc-user1.uvm.edu|vacc-user2.uvm.edu>` 
  - Choose either VACC node - operationally they are identical, 
  performance on a node depends on the number of user logged in to it
  - Use NetID password
- Install this repo
  - `mkdir code`
  - `cd code`
  - `git clone https://github.com/terencebarrett/run_usgs_downloader.git`
  - `cd run_usgs_downloader`
  - `git checkout <branch>`
- Continue setup with step (2) in the section "Setting up USGS Downloader", below

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

Running a batch run on the VACC
-------------------------------
- Slurm documentation: https://slurm.schedmd.com/documentation.html
- VACC guide: https://www.uvm.edu/vacc/kb/knowledge-base/useful-commands/#slurm
- `cd` to root of repo
- Delete the contents of the repo’s *working* folder (the results of the previous run) -- if want to 
start fresh
- Step 1
  - Basic way to run Step 1 on the user node (not recommended after an initial small try)
    - `$ conda activate usgs_downloader`
    - `$ source batch_step_1` (or with another, similar batch file)
  - Proper way to run Step 1 with Slurm that accords with VACC best practices
    - `$ sbatch slurm_step_1.sh`
- Step 2
  - Basic way to run Step 2 using Slurm in an interactive session (not recommended after an initial small try):
    - Start an interactive Slurm run session with 8 cores
      - `srun --nodes=1 --ntasks=1 --cpus-per-task=8 --mail-user=<NetID>@uvm.edu --mail-type=ALL --pty /bin/bash -l`
    - Run Step 2
      - `/users/t/c/<NetID>/miniconda3/condabin/conda run --prefix /users/t/c/<NetID>/miniconda3/envs/usgs_downloader python /users/t/c/<NetID>/code/run_usgs_downloader/run_step_2.py`
    - Exit Slurm run session
      - `exit`
  - Proper way to run Step 2 with Slurm that accords with VACC best practices
    - `$ sbatch slurm_step_2.sh <2-letter-state>`
  - To batch multiple Step 2 Slurm runs
    - This slurm-processes the states sequentially so as not to overwhelm the USGS Entwine server
    - `$ source batch_slurm_step_2.sh`
    
FileZilla settings
------------------
- VM:
  - Protocol: SFTP
  - Host: localhost
  - Port: 2222
  - Logon type: Key file
  - User: vagrant
  - Key file: <path>\run_usgs_downloader\.vagrant\machines\default\virtualbox\private_key
- VACC:
  - Protocol: SFTP
  - Host: vacc-user1.uvm.edu
  - Port: ... leave empty ...
  - Logon type: Ask
  - User: <NetID>
  - Password (when asked): <NetID password>

VM Maintenance
--------------
- When starting the VM, if a message appears to the effect of "Guest Additions version doesn't match that of Host"
  - Install the VB-Guest plugin into the project's Virtual Box, which will keep the Guest Additions version 
  in sync:`vagrant plugin install vagrant-vbguest`
  - When the host's Virtual Box is upgraded, update the plugin with: `vagrant plugin update vagrant-vbguest`
  - If the plugin gets corrupted: `vagrant plugin repair vagrant-vbguest`