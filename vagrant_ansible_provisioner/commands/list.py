from argparse import Namespace
from typing import List

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.role import list_roles


class ListCommand(Command):
    name = "list"

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        roles = list_roles(config.ansible_role_path_host)
        if not roles:
            print("No role found.")
        else:
            print("Available roles:")
            for role in roles:
                print(f" * {role}")
        return 0
