import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import List

from termcolor import cprint

from vagrant_ansible_provisioner.cli import DEFAULT_COMMANDS, Cli
from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.role import apply_role_from_config
from vagrant_ansible_provisioner.utils import exec_or_bail, print_step


class InitializeCommand(Command):
    name = "initialize"

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        print_step("Starting VM")
        exec_or_bail("vagrant up", verbose=verbosity > 0)

        print_step("Applying roles")
        apply_role_from_config(config, "test.role1", as_root=False, verbosity=verbosity, envs=envs)

        cprint("\n✅ Environment is now ready. You can connect to your machine using SSH.", color="green")
        return 0


class LocalCli(Cli):
    def _description(self) -> str:
        return "Custom Sample Cli"

    def _get_known_commands(self) -> List[Command]:
        return [
            InitializeCommand(),
            *DEFAULT_COMMANDS,
        ]

    def _create_extra_subcommands(self, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        subp.add_parser("initialize", help="initialize environment")


def run():
    sys.exit(LocalCli.from_args())
