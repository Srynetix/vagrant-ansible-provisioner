import sys
from argparse import Namespace
from typing import List

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

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        role = args.role
        if not validate_role(config.ansible_role_path_host, args.role):
            cprint(f"Role '{role}' does not exist.\nKnown roles:", color="red", file=sys.stderr)
            for known_role in list_roles(config.ansible_role_path_host):
                cprint(f" * {known_role}", color="red", file=sys.stderr)
            return 1

        apply_role_from_config(
            config,
            role,
            as_root=False,
            verbosity=verbosity,
            envs=envs,
        )
        return 0
