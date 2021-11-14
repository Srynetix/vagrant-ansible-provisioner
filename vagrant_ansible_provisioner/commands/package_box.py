from argparse import ArgumentParser, Namespace, _SubParsersAction

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import exec_or_bail
from vagrant_ansible_provisioner.vagrant import reset_authorized_keys


class PackageBoxCommand(Command):
    name = "package-box"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        box_name: str = args.name
        box_path: str = args.path
        verbosity = config.verbosity.getv()
        self.prepare_box(verbosity)
        self.build_box(box_name, box_path, verbosity)
        return 0

    def prepare_box(self, verbosity: int) -> None:
        # Prior to generating the box, you have to do some things, like adding the Vagrant insecure public key
        reset_authorized_keys(verbose=verbosity > 0)

    def build_box(self, box_name: str, box_path: str, verbosity: int) -> None:
        verbose = verbosity > 0
        exec_or_bail("vagrant halt", verbose=verbose)
        exec_or_bail(f"vagrant package --base {box_name} --output {box_path}", verbose=verbose)

    @staticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        package_box_cmd = subp.add_parser("package-box", help="create a Vagrant box")
        package_box_cmd.add_argument("name", help="box name")
        package_box_cmd.add_argument("path", help="box file path / URL")
