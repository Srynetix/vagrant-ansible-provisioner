from argparse import Namespace

from vagrant_ansible_provisioner.commands.list import ListCommand
from vagrant_ansible_provisioner.config import EnvironmentConfig


def test_list_execute_without_roles(ansible_tmpdir_without_roles: str, capsys):
    config = EnvironmentConfig(ansible_role_path_host=ansible_tmpdir_without_roles)
    out_code = ListCommand().execute(args=Namespace(), config=config)
    captured = capsys.readouterr()
    assert out_code == 0
    assert captured.out == "⚠️  No role found.\n"


def test_list_execute_with_roles(ansible_tmpdir_with_roles, capsys):
    path = ansible_tmpdir_with_roles(["one", "two"])
    config = EnvironmentConfig(ansible_role_path_host=path)
    out_code = ListCommand().execute(args=Namespace(), config=config)
    assert out_code == 0
    captured = capsys.readouterr()
    assert captured.out == ("Available roles:\n" " * one\n" " * two\n")
