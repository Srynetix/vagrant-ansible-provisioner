import sys
from argparse import Namespace
from typing import List

from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.role import list_roles, validate_role
from vagrant_ansible_provisioner.utils import exec_or_bail

from ..command import Command


class ApplyCommand(Command):
    name = "apply"

    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        role = args.role
        if not validate_role(config.ansible_role_path_host, args.role):
            print(f"Role '{role}' does not exist.\nKnown roles:", file=sys.stderr)
            for known_role in list_roles(config.ansible_role_path_host):
                print(f" * {known_role}", file=sys.stderr)
            return 1

        self.apply_role(role, as_root=False, verbosity=verbosity, envs=envs, config=config)
        return 0

    @staticmethod
    def apply_role(role: str, *, as_root: bool, verbosity: int, envs: List[str], config: EnvironmentConfig) -> None:
        role_args = ["-e", f"role={role}"]
        for env in envs:
            role_args.extend(["-e", env])
        role_args_str = " ".join(role_args)

        print(f"▶️ Executing role '{role}' with args '{role_args_str}' ...")
        sudo_cmd = "sudo " if as_root else ""
        verbose_cmd = " -" + verbosity * "v" if verbosity > 0 else ""

        command = (
            f"{sudo_cmd}bash -c 'cd {config.ansible_role_path_guest} "
            f"&& ansible-playbook{verbose_cmd} -i ./inventory ./execute-role.yml {role_args_str}'"
        )

        if config.internal:
            exec_or_bail(command)
        else:
            exec_or_bail(f'vagrant ssh -c "{command}"')
