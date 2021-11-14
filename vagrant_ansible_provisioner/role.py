import json
import os
from collections import OrderedDict
from typing import Any, List, Optional

from vagrant_ansible_provisioner.config import EnvironmentConfig

from .utils import cprint, exec_or_bail


def list_roles(ansible_path: str) -> List[str]:
    roles_dir = os.path.join(ansible_path, "roles")
    return sorted(os.listdir(roles_dir))


def validate_role(ansible_path: str, role: str) -> bool:
    return role in list_roles(ansible_path)


def prepare_env_value(env_key: str, env_value: Any) -> str:
    if isinstance(env_value, bool):
        if env_value:
            env_value = "yes"
        else:
            env_value = "no"

    return f"{env_key}={env_value}"


def generate_playbook_oneline(role: str) -> str:
    playbook = [
        OrderedDict({"hosts": "localhost", "tasks": [OrderedDict({"import_role": OrderedDict({"name": role})})]})
    ]

    return json.dumps(playbook).replace("\n", "")


def generate_role_args(envs: List[str]) -> str:
    role_args = []
    for env in envs:
        role_args.extend(["-e", env])
    return " ".join(role_args)


def generate_ansible_exports(config: EnvironmentConfig) -> str:
    ansible_library = config.ansible_library.getv()

    exports = OrderedDict(
        {
            "ANSIBLE_RETRY_FILES_ENABLED": "False",
            "ANSIBLE_LIBRARY": ansible_library,
            "ANSIBLE_ROLES_PATH": "./roles",
        }
    )

    return " && ".join(f"export {k}={v}" for k, v in exports.items())


def apply_role_from_config(
    config: EnvironmentConfig,
    role: str,
    *,
    as_root: bool = False,
    envs: Optional[List[str]] = None,
) -> None:
    role_path = config.ansible_role_path_guest.getv()
    verbosity = config.verbosity.getv()
    internal = config.internal.getv()

    role_args_str = generate_role_args(envs or [])

    if len(role_args_str) == 0:
        cprint(f"📔 Executing role '{role}' ...", color="blue")
    else:
        role_args_str = f" {role_args_str}"
        cprint(f"📔 Executing role '{role}' with args '{role_args_str}' ...", color="blue")
    print("")

    sudo_cmd = "sudo " if as_root else ""
    verbose_cmd = " -" + verbosity * "v" if verbosity > 0 else ""
    exec_verbose = verbosity > 0

    command = (
        f'{sudo_cmd}bash -c "'
        f"cd {role_path} "
        f"&& {generate_ansible_exports(config)} "
        f"&& ansible-playbook{verbose_cmd} -i ./inventory{role_args_str} /dev/stdin "
        f"<<< $'{generate_playbook_oneline(role)}'"
        f'"'
    )

    if internal:
        exec_or_bail(command, verbose=exec_verbose)
    else:
        exec_or_bail(f"vagrant ssh -c {command}", verbose=exec_verbose)
