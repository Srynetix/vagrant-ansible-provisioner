import configparser
import os
from typing import Any, Generic, Optional, TypeVar

INI_FILE_NAME = "vap.ini"


T = TypeVar("T")


class EnvironmentValue(Generic[T]):
    name: str
    fallback: T
    value: Optional[T]

    def __init__(self, name: str, fallback: T) -> None:
        self.name = name
        self.fallback = fallback
        self.value = None

    def setv(self, value: T):
        self.value = value

    def getv(self) -> T:
        if self.value is None:
            return self.fallback
        return self.value


class EnvironmentConfig:
    ansible_role_path_host: EnvironmentValue[str]
    ansible_role_path_guest: EnvironmentValue[str]
    ansible_library: EnvironmentValue[str]
    remote_user: EnvironmentValue[str]
    verbosity: EnvironmentValue[int]
    internal: EnvironmentValue[bool]

    def __init__(self, **kwargs) -> None:
        self.ansible_role_path_host = EnvironmentValue("ansible_role_path_host", "ansible")
        self.ansible_role_path_guest = EnvironmentValue("ansible_role_path_guest", "/ansible")
        self.ansible_library = EnvironmentValue("ansible_library", "./plugins/modules")
        self.remote_user = EnvironmentValue("remote_user", "vagrant")
        self.verbosity = EnvironmentValue("verbosity", 0)
        self.internal = EnvironmentValue("internal", False)

        for k, v in kwargs.items():
            self.try_set_value(k, v)

    def try_set_value(self, k: str, v: Any) -> None:
        env_value: Optional[EnvironmentValue] = getattr(self, k, None)
        if env_value:
            env_value.setv(v)

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
        remote_user = vagrant
        internal = false
        ```
        """
        config = configparser.ConfigParser()
        config.read(path)

        env_config = EnvironmentConfig()
        for k, v in config.items("environment"):
            env_config.try_set_value(k, v)

        return env_config
