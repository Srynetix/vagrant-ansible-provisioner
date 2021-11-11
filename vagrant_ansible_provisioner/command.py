import abc
from argparse import Namespace
from typing import List

from .config import EnvironmentConfig


class Command(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        """Execute command."""
