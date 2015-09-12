Vagrant.configure("2") do |config|
  config.vm.define :dataproject do |dataproject_config|
    # Every Vagrant virtual environment requires a box to build off of.
    dataproject_config.vm.box = "Trusty64"  #Official Ubuntu 14.04 daily Cloud Image amd64 (Development release, No Guest Additions)

    # The url from where the 'config.vm.box' box will be fetched if it
    # doesn't already exist on the user's system.
    dataproject_config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.provider "virtualbox" do |v|
      host = RbConfig::CONFIG['host_os']

      # Give VM 1/4 system memory & access to all cpu cores on the host
      if host =~ /darwin/
        cpus = `sysctl -n hw.ncpu`.to_i
        # sysctl returns Bytes and we need to convert to MB
        mem = `sysctl -n hw.memsize`.to_i / 1024 / 1024 / 4
      elsif host =~ /linux/
        cpus = `nproc`.to_i
        # meminfo shows KB and we need to convert to MBs
        mem = `grep 'MemTotal' /proc/meminfo | sed -e 's/MemTotal://' -e 's/ kB//'`.to_i / 1024 / 4
      else # sorry Windows folks, I can't help you
        cpus = 2
        mem = 1024
      end

      v.customize ["modifyvm", :id, "--memory", mem]
      v.customize ["modifyvm", :id, "--cpus", cpus]
    end

    config.vbguest.auto_update = true

    config.vm.network "private_network", ip: "10.46.80.80"
    
    # Use NFS for shared folders for better performance
    config.vm.synced_folder '.', '/vagrant', id: "vagrant-root",
    owner: "vagrant",
    group: "www-data",
    mount_options: ["dmode=775,fmode=664"]


    config.vm.network :forwarded_port, guest: 8080, host: 8888
    config.vm.network :forwarded_port, guest: 8000, host: 8001
    config.vm.network :forwarded_port, guest: 9000, host: 9001

    config.berkshelf.enabled = true

    # Enable provisioning with chef solo, specifying a cookbooks path (relative
    # to this Vagrantfile), and adding some recipes and/or roles.
    #
    
    dataproject_config.omnibus.chef_version = :latest

    dataproject_config.vm.provision :shell, :inline => 'apt-get update --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install python-software-properties --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-add-repository ppa:chris-lea/node.js --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-add-repository ppa:mc3man/trusty-media --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install build-essential cmake checkinstall zip unzip ruby1.9.1-dev --no-upgrade --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install libgtk2.0-dev pkg-config libav-tools libavcodec-dev libavformat-dev libswscale-dev --yes' 
    dataproject_config.vm.provision :shell, :inline => 'apt-get install libpq-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev --yes' 
    dataproject_config.vm.provision :shell, :inline => 'apt-get install libevent-dev --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install nodejs --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install libjpeg-dev --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install libmagickwand-dev --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install redis-server --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install git --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install python-pip --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get install postgresql postgresql-contrib --yes'
    dataproject_config.vm.provision :shell, :inline => 'apt-get autoremove --yes'

    dataproject_config.vm.provision :chef_solo do |chef|

    chef.add_recipe "apt"
    chef.add_recipe "build-essential"
    chef.add_recipe "yum"
    chef.add_recipe "aws"
    chef.add_recipe "chef-sugar"
    chef.add_recipe "postgresql"
    chef.add_recipe "xfs"
    chef.add_recipe "apache2"
    chef.add_recipe "git"
    chef.add_recipe "database"
    chef.add_recipe "postgresql::server"
    chef.add_recipe "postgresql::client"
    chef.add_recipe "app"

    chef.json = {
      python: {
        install_method: 'source',
        version: '2.7.5',
        checksum: 'b4f01a1d0ba0b46b05c73b2ac909b1df'
      },
      postgresql: {
        password:   {
          postgres:   'postgres',
        },
      },
      app: {
        db: {
          name: "dataproject"
        }
      }
    }

    end

    dataproject_config.vm.provision :shell, :inline => 'pip install -r /vagrant/pip-requirements.txt'
    
    
  end
end