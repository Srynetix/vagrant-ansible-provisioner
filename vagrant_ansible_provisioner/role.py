import json
import os
from typing import Any, List

from vagrant_ansible_provisioner.config import EnvironmentConfig

from .utils import cprint, exec_or_bail


def list_roles(ansible_path: str) -> List[str]:
    roles_dir = os.path.join(ansible_path, "roles")
    return sorted(list(os.listdir(roles_dir)))


def validate_role(ansible_path: str, role: str) -> bool:
    return role in list_roles(ansible_path)


def prepare_env_value(env_key: str, env_value: Any) -> str:
    if isinstance(env_value, bool):
        if env_value:
            env_value = "yes"
        else:
            env_value = "no"

    return f"{env_key}={env_value}"


def apply_role(
    role_path: str,
    role: str,
    *,
    as_root: bool,
    verbosity: int,
    envs: List[str],
    internal: bool,
) -> None:
    envs = envs or []
    role_args = []
    for env in envs:
        role_args.extend(["-e", env])
    role_args_str = " ".join(role_args)

    if len(role_args) == 0:
        cprint(f"📔 Executing role '{role}' ...", color="blue")
    else:
        role_args_str = f" {role_args_str}"
        cprint(f"📔 Executing role '{role}' with args '{role_args_str}' ...", color="blue")
    print("")

    sudo_cmd = "sudo " if as_root else ""
    verbose_cmd = " -" + verbosity * "v" if verbosity > 0 else ""
    exec_verbose = verbosity > 0
    playbook = [{"hosts": "localhost", "tasks": [{"import_role": {"name": role}}]}]
    playbook_oneline = json.dumps(playbook).replace("\n", "")

    command = (
        f'{sudo_cmd}bash -c "'
        f"cd {role_path} "
        f"&& export ANSIBLE_RETRY_FILES_ENABLED=False "
        f"&& export ANSIBLE_ROLES_PATH=./roles "
        f"&& ansible-playbook{verbose_cmd} -i ./inventory{role_args_str} /dev/stdin <<< $'{playbook_oneline}'"
        f'"'
    )

    if internal:
        exec_or_bail(command, verbose=exec_verbose)
    else:
        exec_or_bail(f"vagrant ssh -c {command}", verbose=exec_verbose)


def apply_role_from_config(
    config: EnvironmentConfig,
    role: str,
    *,
    as_root: bool,
    verbosity: int,
    envs: List[str],
) -> None:
    apply_role(
        config.ansible_role_path_guest, role, as_root=as_root, verbosity=verbosity, envs=envs, internal=config.internal
    )
