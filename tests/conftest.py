import os
from typing import List

import pytest


@pytest.fixture
def ansible_tmpdir_with_roles(tmpdir):
    def _inner(role_list: List[str]):
        roles = tmpdir.join("roles")
        os.makedirs(roles)
        for role in role_list:
            os.makedirs(roles.join(role))
        return tmpdir

    return _inner


@pytest.fixture
def ansible_tmpdir_without_roles(tmpdir):
    roles = tmpdir.join("roles")
    os.makedirs(roles)
    return tmpdir
