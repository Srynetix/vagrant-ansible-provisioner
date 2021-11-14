from argparse import Namespace

from vagrant_ansible_provisioner.commands.apply import ApplyCommand
from vagrant_ansible_provisioner.config import EnvironmentConfig


def test_execute_missing_role(exec_or_bail_mock, ansible_tmpdir_with_roles, capsys):
    path = ansible_tmpdir_with_roles(["one", "two"])
    config = EnvironmentConfig(ansible_role_path_host=path)
    args = Namespace(role="three", env=None)
    out_code = ApplyCommand().execute(args=args, config=config)
    captured = capsys.readouterr()

    assert len(exec_or_bail_mock) == 0
    assert out_code == 1
    assert captured.err == ("Role 'three' does not exist.\n" "Known roles:\n" " * one\n" " * two\n")


def test_execute_known_role(exec_or_bail_mock, ansible_tmpdir_with_roles, capsys):
    path = ansible_tmpdir_with_roles(["one", "two"])
    config = EnvironmentConfig(ansible_role_path_host=path)
    args = Namespace(role="one", env=None)
    out_code = ApplyCommand().execute(args=args, config=config)
    captured = capsys.readouterr()

    assert len(exec_or_bail_mock) == 1
    assert out_code == 0
    assert captured.out == ("📔 Executing role 'one' ...\n\n")
