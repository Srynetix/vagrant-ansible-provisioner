import sys
from argparse import ArgumentParser, Namespace, _SubParsersAction

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.role import (
    apply_role_from_config,
    list_roles,
    validate_role,
)
from vagrant_ansible_provisioner.utils import cprint


class ApplyCommand(Command):
    name = "apply"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        envs = args.env or []
        role = args.role

        if not validate_role(config.ansible_role_path_host.getv(), args.role):
            cprint(f"Role '{role}' does not exist.\nKnown roles:", color="red", file=sys.stderr)
            for known_role in list_roles(config.ansible_role_path_host.getv()):
                cprint(f" * {known_role}", color="red", file=sys.stderr)
            return 1

        apply_role_from_config(
            config,
            role,
            as_root=False,
            envs=envs,
        )
        return 0

    @staticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        apply_cmd = subp.add_parser("apply", help="apply Ansible role")
        apply_cmd.add_argument("role", help="role name (from ./playbook/roles)")
        apply_cmd.add_argument("-e", "--env", action="append", help="set environment value (eg. VAR=1)")
