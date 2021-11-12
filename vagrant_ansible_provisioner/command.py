import abc
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import List

from .config import EnvironmentConfig


class Command(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, verbosity: int, envs: List[str], config: EnvironmentConfig, args: Namespace) -> int:
        """Execute command."""

    @staticmethod
    @abc.abstractstaticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        """Add arguments."""
