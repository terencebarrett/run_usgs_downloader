Vagrant.configure("2") do |config|

  config.vm.box = "generic/rhel7"
  config.vm.synced_folder ".", "/vagrant"

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.name = "RedHat Enterprise 7.9"
    vb.memory = 25576
    vb.cpus = 6

  end

end
