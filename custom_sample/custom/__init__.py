from argparse import _SubParsersAction, ArgumentParser, Namespace
import sys
from typing import List

from colorama import Fore

from vagrant_ansible_provisioner.cli import DEFAULT_COMMANDS, Cli
from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import exec_or_bail, print_step
from vagrant_ansible_provisioner.role import apply_role_from_config


class InitializeCommand(Command):
    name = "initialize"

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        print_step("Starting VM")
        exec_or_bail("vagrant up", verbose=verbosity > 0)

        print_step("Applying roles")
        apply_role_from_config(config, "test.role1", as_root=False, verbosity=verbosity, envs=envs)

        print(Fore.GREEN + "\n✅ Environment is now ready. You can connect to your machine using SSH." + Fore.RESET)
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
