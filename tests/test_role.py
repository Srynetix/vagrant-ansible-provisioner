from vagrant_ansible_provisioner.role import (
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
