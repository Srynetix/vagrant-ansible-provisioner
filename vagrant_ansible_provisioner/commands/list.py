from argparse import ArgumentParser, Namespace, _SubParsersAction

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.role import list_roles
from vagrant_ansible_provisioner.utils import print_info, print_warn


class ListCommand(Command):
    name = "list"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        path = config.ansible_role_path_host.getv()
        if config.internal.getv():
            path = config.ansible_role_path_guest.getv()

        roles = list_roles(path)
        if not roles:
            print_warn("No role found.")
        else:
            print_info("Available roles:", prefix="")
            for role in roles:
                print_info(role, prefix=" *")
        return 0

    @classmethod
    def add_arguments(cls, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        subp.add_parser("list", help="list Ansible roles")
