import sys
from argparse import ArgumentParser
from typing import List, Optional, Sequence, Type

from vagrant_ansible_provisioner.commands.install_box import InstallBoxCommand
from vagrant_ansible_provisioner.commands.package_box import PackageBoxCommand
from vagrant_ansible_provisioner.config import EnvironmentConfig

from .command import Command
from .commands.apply import ApplyCommand
from .commands.list import ListCommand
from .version import __version__

DEFAULT_COMMANDS: List[Type[Command]] = [ApplyCommand, ListCommand, PackageBoxCommand, InstallBoxCommand]


class Cli:
    def _description(self) -> str:
        return "Vagrant Ansible Provisioner"

    def _get_configuration(self) -> EnvironmentConfig:
        return EnvironmentConfig.from_current_dir()

    def _get_known_commands(self) -> List[Type[Command]]:
        return DEFAULT_COMMANDS

    def _create_subcommands(self, parser: ArgumentParser, commands: List[Type[Command]]) -> None:
        subp = parser.add_subparsers(dest="command")

        for command in commands:
            command.add_arguments(parser, subp)

    def _create_parser(self, commands: List[Type[Command]]) -> ArgumentParser:
        parser = ArgumentParser(description=self._description())
        self._create_subcommands(parser, commands)

        parser.add_argument(
            "-V", "--version", action="version", version="%(prog)s {version}".format(version=__version__)
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

        command = parsed_args.command
        verbosity = min(parsed_args.verbose, 3)
        envs = getattr(parsed_args, "env", None) or []

        if command is not None:
            for known_command in known_commands:
                if command == known_command.name:
                    cmd_instance = known_command()
                    return cmd_instance.execute(verbosity, envs, config, parsed_args)

            # Unknown command
            print(f"Unimplemented command '{command}'.", file=sys.stderr)
            return 2

        else:
            # Command is missing
            parser.print_help()
            return 1


def run():
    sys.exit(Cli.from_args())
