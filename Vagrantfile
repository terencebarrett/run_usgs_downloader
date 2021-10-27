Vagrant.configure("2") do |config|

  config.vm.box = "generic/rhel7"
  config.vm.synced_folder ".", "/vagrant"

  # Optionally configure other folders to share between host and VM
  # Note: Use \\ as the separator for Windows paths
  config.vm.synced_folder "C:\\Users\\tcbarret\\PycharmProjects\\lidar_dataprep", "/vagrant/lidar_dataprep"
  config.vm.synced_folder "D:", "/vagrant/Ddrive"
  config.vm.synced_folder "E:", "/vagrant/Edrive"
  config.vm.synced_folder "O:", "/vagrant/Odrive"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.name = "RedHat Enterprise 7.9"
    vb.memory = 25576
    vb.cpus = 6

  end

end
