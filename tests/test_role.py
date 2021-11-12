from vagrant_ansible_provisioner.role import (
    apply_role,
    list_roles,
    prepare_env_value,
    validate_role,
)


def test_list_roles(ansible_tmpdir_with_roles):
    path = ansible_tmpdir_with_roles(["one", "two"])
    assert list_roles(path) == ["one", "two"]


def test_validate_role(ansible_tmpdir_with_roles):
    path = ansible_tmpdir_with_roles(["one", "two"])
    assert validate_role(path, "one")
    assert not validate_role(path, "three")


def test_prepare_env_value():
    assert prepare_env_value("one", "1") == "one=1"
    assert prepare_env_value("one", 1) == "one=1"
    assert prepare_env_value("one", 0.5) == "one=0.5"
    assert prepare_env_value("one", True) == "one=yes"
    assert prepare_env_value("one", False) == "one=no"


def test_apply_role_no_env(exec_or_bail_mock):
    apply_role("/tmp", "one", as_root=False, verbosity=0, envs=[], internal=False)

    assert exec_or_bail_mock.pop() == (
        (
            'vagrant ssh -c bash -c "cd /tmp '
            "&& export ANSIBLE_RETRY_FILES_ENABLED=False "
            "&& export ANSIBLE_ROLES_PATH=./roles "
            "&& ansible-playbook -i ./inventory /dev/stdin "
            '<<< $\'[{"hosts": "localhost", "tasks": [{"import_role": {"name": "one"}}]}]\'"'
        ),
        {"verbose": False},
    )


def test_apply_role_env(exec_or_bail_mock):
    apply_role("/tmp", "one", as_root=False, verbosity=0, envs=["a=1", "pouet=yes"], internal=False)

    assert exec_or_bail_mock.pop() == (
        (
            'vagrant ssh -c bash -c "cd /tmp '
            "&& export ANSIBLE_RETRY_FILES_ENABLED=False "
            "&& export ANSIBLE_ROLES_PATH=./roles "
            "&& ansible-playbook -i ./inventory -e a=1 -e pouet=yes /dev/stdin "
            '<<< $\'[{"hosts": "localhost", "tasks": [{"import_role": {"name": "one"}}]}]\'"'
        ),
        {"verbose": False},
    )


def test_apply_role_verbosity(exec_or_bail_mock):
    apply_role("/tmp", "one", as_root=False, verbosity=3, envs=[], internal=False)

    assert exec_or_bail_mock.pop() == (
        (
            'vagrant ssh -c bash -c "cd /tmp '
            "&& export ANSIBLE_RETRY_FILES_ENABLED=False "
            "&& export ANSIBLE_ROLES_PATH=./roles "
            "&& ansible-playbook -vvv -i ./inventory /dev/stdin "
            '<<< $\'[{"hosts": "localhost", "tasks": [{"import_role": {"name": "one"}}]}]\'"'
        ),
        {"verbose": True},
    )


def test_apply_role_as_root(exec_or_bail_mock):
    apply_role("/tmp", "one", as_root=True, verbosity=0, envs=[], internal=False)

    assert exec_or_bail_mock.pop() == (
        (
            'vagrant ssh -c sudo bash -c "cd /tmp '
            "&& export ANSIBLE_RETRY_FILES_ENABLED=False "
            "&& export ANSIBLE_ROLES_PATH=./roles "
            "&& ansible-playbook -i ./inventory /dev/stdin "
            '<<< $\'[{"hosts": "localhost", "tasks": [{"import_role": {"name": "one"}}]}]\'"'
        ),
        {"verbose": False},
    )


def test_apply_role_internal(exec_or_bail_mock):
    apply_role("/tmp", "one", as_root=False, verbosity=0, envs=[], internal=True)

    assert exec_or_bail_mock.pop() == (
        (
            'bash -c "cd /tmp '
            "&& export ANSIBLE_RETRY_FILES_ENABLED=False "
            "&& export ANSIBLE_ROLES_PATH=./roles "
            "&& ansible-playbook -i ./inventory /dev/stdin "
            '<<< $\'[{"hosts": "localhost", "tasks": [{"import_role": {"name": "one"}}]}]\'"'
        ),
        {"verbose": False},
    )
