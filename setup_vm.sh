# Accept all defaults, apart from replying 'yes' to the running of `conda init`
# After conda install `exit` the ssh session and re-enter (`vagrant ssh`)
#   to be able to use conda (or add command here to refresh the session)
wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh