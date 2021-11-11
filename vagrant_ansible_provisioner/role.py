import os
from typing import Any, List


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
