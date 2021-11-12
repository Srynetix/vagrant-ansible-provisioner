from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import List

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import exec_or_bail


class InstallBoxCommand(Command):
    name = "install-box"

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        box_name: str = args.name
        box_path: str = args.path

        exec_or_bail(f"vagrant box add --name {box_name} -f {box_path}")
        return 0

    @staticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        install_box_cmd = subp.add_parser("install-box", help="install a Vagrant box")
        install_box_cmd.add_argument("name", help="box name")
        install_box_cmd.add_argument("path", help="box file path / URL")
