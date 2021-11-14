from distutils.core import setup

from .vagrant_ansible_provisioner.version import __version__

setup(
    name="vagrant-ansible-provisioner",
    version=__version__,
    packages=[
        "vagrant_ansible_provisioner",
        "vagrant_ansible_provisioner.commands",
    ]
)
