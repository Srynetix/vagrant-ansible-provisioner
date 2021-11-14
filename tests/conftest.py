import os
from typing import Any, List

import pytest


@pytest.fixture(autouse=True)
def _disable_colors(monkeypatch):
    def _cprint(*args, **kwargs):
        if "color" in kwargs:
            kwargs.pop("color")
        print(*args, **kwargs)

    def _colored(text, *args, **kwargs):
        return text

    monkeypatch.setattr("vagrant_ansible_provisioner.utils._colored", _colored)
    monkeypatch.setattr("vagrant_ansible_provisioner.utils._cprint", _cprint)


@pytest.fixture()
def ansible_tmpdir_with_roles(tmpdir):
    def _inner(role_list: List[str]):
        roles = tmpdir.join("roles")
        os.makedirs(roles)
        for role in role_list:
            os.makedirs(roles.join(role))
        return tmpdir

    return _inner


@pytest.fixture()
def ansible_tmpdir_without_roles(tmpdir):
    roles = tmpdir.join("roles")
    os.makedirs(roles)
    return tmpdir


@pytest.fixture()
def mock_and_trace_calls(monkeypatch):
    def inner(path: str, return_value: Any = None):
        calls = []

        def _fn(*args, **kwargs):
            calls.append((*args, {**kwargs}))
            return return_value

        monkeypatch.setattr(path, _fn)
        return calls

    return inner


@pytest.fixture()
def exec_or_bail_mock(mock_and_trace_calls):
    return mock_and_trace_calls("vagrant_ansible_provisioner.role.exec_or_bail")
