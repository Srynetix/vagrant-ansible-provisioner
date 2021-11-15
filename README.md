# vagrant-ansible-provisioner

[![Checks](https://github.com/Srynetix/vagrant-ansible-provisioner/actions/workflows/checks.yml/badge.svg)](https://github.com/Srynetix/vagrant-ansible-provisioner/actions/workflows/checks.yml)
[![Coverage Status](https://coveralls.io/repos/github/Srynetix/vagrant-ansible-provisioner/badge.svg)](https://coveralls.io/github/Srynetix/vagrant-ansible-provisioner)
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
- As role path on the host (`ansible_role_path_host`): `"./ansible"`
- As role path on the guest (`ansible_role_path_guest`): `"/ansible"`
- As Ansible library path (`ansible_library`): `"./plugins/modules"`
- As remote user (remote_user): `"vagrant"`

Here is a sample Vagrantfile (based on an Ubuntu 20.04 box):

```ruby
Vagrant.configure("2") do |config|
    config.vm.define "machine-name" do |s|
        s.vm.box = "bento/ubuntu-20.04"
        s.vm.provision :shell, inline: "sudo apt update && sudo apt install ansible -y"
        s.vm.synced_folder "./ansible", "/ansible", mount_options: ["dmode=775,fmode=664"]
    end
end
```

Then, you can use this project directly from the command-line executable `vagrant-ansible-provisioner`, in a folder containing a `Vagrantfile`.

```bash
vagrant-ansible-provisioner apply my.role
```

The command-line executable has two commands:

- `apply role [-e ENV ...]`: Apply a role (with optional environment variables)
- `list`: List available roles (in `ansible_role_path_host` folder)
- `port-forward port [port ...]`: Utility command to expose one or multiple ports from the guest to the host
- `package-box --vm-name VM_NAME --box-name BOX_NAME --box-description BOX_DESCRIPTION --box-version BOX_VERSION [--box-engine BOX_ENGINE] [--box-url BOX_URL] box_path`: Build a Vagrant box from one of the declared machines in the Vagrantfile
- `install-box path`: Install a Vagrant box from a JSON path or URL

### Ad-hoc use

You can also create an ad-hoc Python module on your project, and inherit the `Cli` class with custom arguments.
There is a complete example in the [`custom_sample`](./custom_sample) folder, with a `Vagrantfile` included.
