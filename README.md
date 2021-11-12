# vagrant-ansible-provisioner

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Parametrable Ansible provisioner to use with a Vagrant box.

## What ?

It is a small wrapper around `ansible-playbook` to execute roles locally on a Vagrant Box.

## Requirements ?

- Python 3.9

### For contributing

- `just` command runner - https://github.com/casey/just

## How to use ?

You need to setup a shared folder to have access to your roles, and have `ansible` installed.
Default configuration is to have:
- As a role path on the host (ansible_role_path_host): "./ansible"
- As a role path on the guest (ansible_role_path_guest): "/ansible"

Here is a sample Vagrantfile (based on an Ubuntu 20.04 box):

```ruby
$SHELL_PROV = <<-SCRIPT
sudo apt update
sudo apt install python3-pip -y
sudo python3 -m pip install ansible
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.define "machine-name" do |s|
        s.vm.box = "bento/ubuntu-20.04"

        s.vm.provision :shell, inline: $SHELL_PROV
        s.vm.synced_folder "./ansible", "/ansible", mount_options: ["dmode=775,fmode=664"]
    end
end
```

Then, you can use this project directly from the command-line executable `vagrant-ansible-provisioner`, in a folder containing a `Vagrantfile`.

```bash
vagrant-ansible-provisioner apply my.role
```

The command-line executable has two commands:

- `apply <role-name> [-e env-name=env-value]`: Apply a role (with optional environment variables)
- `list`: List roles

### Ad-hoc use

You can also create an ad-hoc Python module on your project, and inherit the `Cli` class with custom arguments.
There is a complete example in the [`custom_sample`](./custom_sample) folder, with a `Vagrantfile` included.
