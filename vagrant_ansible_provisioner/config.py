import configparser
import os

INI_FILE_NAME = "vap.ini"


class EnvironmentConfig:
    ansible_role_path_host: str
    ansible_role_path_guest: str
    internal: bool

    def __init__(
        self,
        *,
        ansible_role_path_host: str = "ansible",
        ansible_role_path_guest: str = "/ansible",
        internal: bool = False,
    ) -> None:
        self.ansible_role_path_host = ansible_role_path_host
        self.ansible_role_path_guest = ansible_role_path_guest
        self.internal = internal

    @classmethod
    def default(cls) -> "EnvironmentConfig":
        return EnvironmentConfig()

    @classmethod
    def from_current_dir(cls) -> "EnvironmentConfig":
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, INI_FILE_NAME)
        if os.path.exists(config_path):
            return cls.from_file(config_path)
        else:
            return cls.default()

    @classmethod
    def from_file(cls, path: str) -> "EnvironmentConfig":
        """
        File example:

        ```
        [environment]
        ansible_role_path_host = ansible
        ansible_role_path_guest = /ansible
        internal = true
        ```
        """
        config = configparser.ConfigParser()
        config.read(path)

        return EnvironmentConfig(
            ansible_role_path_host=config.get("environment", "ansible_role_path_host", fallback="ansible"),
            ansible_role_path_guest=config.get("environment", "ansible_role_path_guest", fallback="/ansible"),
            internal=config.getboolean("environment", "internal", fallback=False),
        )
