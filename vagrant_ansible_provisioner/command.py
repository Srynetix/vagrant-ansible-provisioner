import abc
from argparse import ArgumentParser, Namespace, _SubParsersAction

from .config import EnvironmentConfig


class Command(abc.ABC):
    name: str

    @abc.abstractmethod
    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        """Execute command."""

    @classmethod
    @abc.abstractclassmethod
    def add_arguments(cls, parser: ArgumentParser, subp: _SubParsersAction) -> None:
        """Add arguments."""
