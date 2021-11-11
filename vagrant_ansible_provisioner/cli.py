import sys
from argparse import ArgumentParser, _SubParsersAction
from typing import List, Optional, Sequence

from vagrant_ansible_provisioner.config import EnvironmentConfig

from .command import Command
from .commands.apply import ApplyCommand
from .commands.list import ListCommand
from .version import __version__

DEFAULT_COMMANDS = [ApplyCommand(), ListCommand()]


class CliConfig:
    environment_config: EnvironmentConfig
    known_commands: List[Command]

    def __init__(self, *, environment_config: EnvironmentConfig = None, known_commands: List[Command] = None) -> None:
        if environment_config is None:
            environment_config = EnvironmentConfig.from_current_dir()
        self.environment_config = environment_config
        self.known_commands = known_commands or DEFAULT_COMMANDS


class Cli:
    config: CliConfig

    def __init__(self, config: CliConfig = None) -> None:
        if config is None:
            config = CliConfig()
        self.config = config

    def _create_subcommands(self, parser: ArgumentParser) -> None:
        subp = parser.add_subparsers(dest="command")
        self._create_base_subcommands(parser, subp)
        self._create_extra_subcommands(parser, subp)

    def _add_environment_arg(self, parser: ArgumentParser) -> None:
        parser.add_argument("-e", "--env", action="append", help="set environment value (eg. VAR=1)")

    def _create_base_subcommands(self, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        apply_cmd = subp.add_parser("apply", help="apply Ansible role")
        apply_cmd.add_argument("role", help="role name (from ./playbook/roles)")
        self._add_environment_arg(apply_cmd)

        subp.add_parser("list", help="list Ansible roles")

    def _create_extra_subcommands(self, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        pass

    def _create_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description="Vagrant Ansible Provisioner")
        self._create_subcommands(parser)

        parser.add_argument(
            "-V", "--version", action="version", version="%(prog)s {version}".format(version=__version__)
        )
        parser.add_argument("-v", "--verbose", action="count", help="verbosity (up to 3)", default=0)

        return parser

    @classmethod
    def from_args_with_config(cls, config: CliConfig, args: Optional[Sequence[str]] = None) -> int:
        cli = cls()
        parser = cli._create_parser()
        parsed_args = parser.parse_args(args)

        command = parsed_args.command
        verbosity = min(parsed_args.verbose, 3)
        envs = getattr(parsed_args, "env", [])

        if command is not None:
            for known_command in cli.config.known_commands:
                if command == known_command.name:
                    return known_command.execute(verbosity, envs, cli.config.environment_config, parsed_args)

            # Unknown command
            print(f"Unimplemented command '{command}'.", file=sys.stderr)
            return 2

        else:
            # Command is missing
            parser.print_help()
            return 1

    @classmethod
    def from_args(cls, args: Optional[Sequence[str]] = None) -> int:
        return cls.from_args_with_config(CliConfig(), args)


def run():
    sys.exit(Cli.from_args())
