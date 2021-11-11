from argparse import Namespace

import pytest

from vagrant_ansible_provisioner.commands.apply import ApplyCommand
from vagrant_ansible_provisioner.config import EnvironmentConfig


@pytest.fixture
def exec_or_bail_mock(monkeypatch):
    calls = []

    def exec_or_bail_mock(command):
        calls.append(command)

    monkeypatch.setattr("vagrant_ansible_provisioner.commands.apply.exec_or_bail", exec_or_bail_mock)
    return calls


def test_apply_role_no_env(exec_or_bail_mock):
    ApplyCommand.apply_role(
        "one", as_root=False, verbosity=0, envs=[], config=EnvironmentConfig(ansible_role_path_guest="/tmp")
    )

    assert (
        exec_or_bail_mock.pop()
        == "vagrant ssh -c \"bash -c 'cd /tmp && ansible-playbook -i ./inventory ./execute-role.yml -e role=one'\""
    )


def test_apply_role_env(exec_or_bail_mock):
    ApplyCommand.apply_role(
        "one",
        as_root=False,
        verbosity=0,
        envs=["a=1", "pouet=yes"],
        config=EnvironmentConfig(ansible_role_path_guest="/tmp"),
    )

    assert exec_or_bail_mock.pop() == (
        "vagrant ssh -c \"bash -c 'cd /tmp && ansible-playbook "
        "-i ./inventory ./execute-role.yml -e role=one -e a=1 -e pouet=yes'\""
    )


def test_apply_role_verbosity(exec_or_bail_mock):
    ApplyCommand.apply_role(
        "one", as_root=False, verbosity=3, envs=[], config=EnvironmentConfig(ansible_role_path_guest="/tmp")
    )

    assert (
        exec_or_bail_mock.pop()
        == "vagrant ssh -c \"bash -c 'cd /tmp && ansible-playbook -vvv -i ./inventory ./execute-role.yml -e role=one'\""
    )


def test_apply_role_as_root(exec_or_bail_mock):
    ApplyCommand.apply_role(
        "one", as_root=True, verbosity=0, envs=[], config=EnvironmentConfig(ansible_role_path_guest="/tmp")
    )

    assert (
        exec_or_bail_mock.pop()
        == "vagrant ssh -c \"sudo bash -c 'cd /tmp && ansible-playbook -i ./inventory ./execute-role.yml -e role=one'\""
    )


def test_apply_role_internal(exec_or_bail_mock):
    ApplyCommand.apply_role(
        "one",
        as_root=False,
        verbosity=0,
        envs=[],
        config=EnvironmentConfig(ansible_role_path_guest="/tmp", internal=True),
    )

    assert (
        exec_or_bail_mock.pop() == "bash -c 'cd /tmp && ansible-playbook -i ./inventory ./execute-role.yml -e role=one'"
    )


def test_execute_missing_role(exec_or_bail_mock, ansible_tmpdir_with_roles, capsys):
    path = ansible_tmpdir_with_roles(["one", "two"])
    config = EnvironmentConfig(ansible_role_path_host=path)
    args = Namespace(role="three")
    out_code = ApplyCommand().execute(verbosity=0, envs=[], config=config, args=args)
    captured = capsys.readouterr()

    assert len(exec_or_bail_mock) == 0
    assert out_code == 1
    assert captured.err == ("Role 'three' does not exist.\n" "Known roles:\n" " * one\n" " * two\n")


def test_execute_known_role(exec_or_bail_mock, ansible_tmpdir_with_roles, capsys):
    path = ansible_tmpdir_with_roles(["one", "two"])
    config = EnvironmentConfig(ansible_role_path_host=path)
    args = Namespace(role="one")
    out_code = ApplyCommand().execute(verbosity=0, envs=[], config=config, args=args)
    captured = capsys.readouterr()

    assert len(exec_or_bail_mock) == 1
    assert out_code == 0
    assert captured.out == ("▶️ Executing role 'one' with args '-e role=one' ...\n")
