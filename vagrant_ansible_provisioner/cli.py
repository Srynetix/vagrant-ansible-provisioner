import os
import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from typing import List, Optional, Sequence, Type

from vagrant_ansible_provisioner.commands.install_box import InstallBoxCommand
from vagrant_ansible_provisioner.commands.package_box import PackageBoxCommand
from vagrant_ansible_provisioner.commands.port_forward import PortForwardCommand
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import print_error

from .command import Command
from .commands.apply import ApplyCommand
from .commands.list import ListCommand
from .version import __version__

DEFAULT_COMMANDS: List[Type[Command]] = [
    ApplyCommand,
    ListCommand,
    PortForwardCommand,
    PackageBoxCommand,
    InstallBoxCommand,
]


def get_default_commands(without: List[Type[Command]]) -> List[Type[Command]]:
    return [cmd for cmd in DEFAULT_COMMANDS if cmd not in without]


class Cli:
    def _description(self) -> str:
        return "Vagrant Ansible Provisioner"

    def _get_prog_name(self) -> str:
        return os.path.basename(sys.argv[0])

    def _get_version(self) -> str:
        return __version__

    def _get_configuration(self) -> EnvironmentConfig:
        return EnvironmentConfig.from_current_dir()

    def _get_known_commands(self) -> List[Type[Command]]:
        return DEFAULT_COMMANDS

    def _create_subcommands(self, parser: ArgumentParser, commands: List[Type[Command]]) -> None:
        subp = parser.add_subparsers(dest="command")

        for command in commands:
            command.add_arguments(parser, subp)

    def _create_parser(self, commands: List[Type[Command]]) -> ArgumentParser:
        parser = ArgumentParser(description=self._description(), formatter_class=ArgumentDefaultsHelpFormatter)
        self._create_subcommands(parser, commands)

        parser.add_argument(
            "-V",
            "--version",
            action="version",
            version="{prog} {version}".format(prog=self._get_prog_name(), version=self._get_version()),
        )
        parser.add_argument("-v", "--verbose", action="count", help="verbosity (up to 3)", default=0)

        return parser

    @classmethod
    def from_args(cls, args: Optional[Sequence[str]] = None) -> int:
        cli = cls()
        known_commands = cli._get_known_commands()
        parser = cli._create_parser(known_commands)
        config = cli._get_configuration()
        parsed_args = parser.parse_args(args)

        # Clamp verbosity to 3
        verbosity = config.verbosity.getv()
        if parsed_args.verbose > 0:
            verbosity = parsed_args.verbose
        verbosity = min(verbosity, 3)
        config.verbosity.setv(verbosity)

        command = parsed_args.command

        if command is not None:
            for known_command in known_commands:
                if command == known_command.name:
                    cmd_instance = known_command()
                    return cmd_instance.execute(parsed_args, config)

            # Unknown command
            print_error(f"Unimplemented command '{command}'.")
            return 2

        else:
            # Command is missing
            parser.print_help()
            return 1


def run() -> None:
    sys.exit(Cli.from_args())
