from vagrant_ansible_provisioner.cli import Cli


def test_cli_missing_command():
    assert Cli.from_args([]) == 1
