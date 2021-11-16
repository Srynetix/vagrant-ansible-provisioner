from setuptools import setup

setup(
    package_data={"vagrant_ansible_provisioner": ["py.typed"]},
    packages=[
        "vagrant_ansible_provisioner",
        "vagrant_ansible_provisioner.commands",
    ],
    zip_safe=False,
)
