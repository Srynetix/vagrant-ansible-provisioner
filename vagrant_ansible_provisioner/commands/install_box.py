from argparse import ArgumentParser, Namespace, _SubParsersAction

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import exec_or_bail


class InstallBoxCommand(Command):
    name = "install-box"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        box_path: str = args.path

        exec_or_bail(f"vagrant box add -f {box_path}")
        return 0

    @classmethod
    def add_arguments(cls, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        install_box_cmd = subp.add_parser("install-box", help="install a Vagrant box from JSON")
        install_box_cmd.add_argument("path", help="box JSON file path / URL")
