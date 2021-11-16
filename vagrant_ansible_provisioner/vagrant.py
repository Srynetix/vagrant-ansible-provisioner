import hashlib
import os
import subprocess
from typing import Any, Dict, Optional

from .utils import bail, exec_or_bail, print_info

INSECURE_PUBLIC_KEY = """
ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEA6NF8iallvQVp22WDkTkyrtvp9eWW6A8YVr+kz4TjGYe7gHzIw+niNltGEFHzD8+v1I2YJ6oXevct1YeS0o9HZyN1Q9qgCgzUFtdOKLv6IedplqoPkcmF0aYet2PkEDo3MlTBckFXPITAMzF8dJSIFo9D8HfdOV0IAdx4O7PtixWKn5y2hMNG0zQPyUecp4pzC6kivAIhyfHilFR61RGL+GPXQ2MWZWFYbAGjyiYJnAmCP3NOTd0jMZEnDkbUvxhMmBYSdETk1rRgm+R4LOzFUGaHqHDLKLX+FIPKcF96hrucXzcWyLbIbEgE98OHlnVYCzRdK8jlqm8tehUc9c9WhQ== vagrant insecure public key
"""[  # noqa: E501
    1:-1
]


def reset_authorized_keys(*, verbose: bool = False) -> None:
    print_info("Resetting authorized_keys with vagrant insecure public key ...")
    exec_or_bail(f"vagrant ssh -c \"echo '{INSECURE_PUBLIC_KEY}' > ~/.ssh/authorized_keys\"", verbose=verbose)


def generate_sha(path: str) -> str:
    s = hashlib.sha256()
    block_size = 4096
    with open(path, mode="rb") as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            s.update(buf)
            buf = f.read(block_size)
    return s.hexdigest()


def generate_box_manifest(
    *, name: str, description: str, version: str, path: str, engine: str, url: Optional[str] = None
) -> Dict[str, Any]:
    if not os.path.isfile(path):
        raise IOError(f"Missing file at path '{path}'.")

    print_info(f"Generating SHA256 hash of file '{path}' ...")
    checksum = generate_sha(path)

    return {
        "name": name,
        "description": description,
        "versions": [
            {
                "version": version,
                "providers": [{"name": engine, "url": url or path, "checksum_type": "sha256", "checksum": checksum}],
            }
        ],
    }


def upload_file_to_guest(src: str, dest: str, *, vm_name: Optional[str] = None, verbose: bool = False) -> None:
    cmd = f'vagrant upload "{src}" "{dest}"'
    if vm_name is not None:
        cmd = f'{cmd} "{vm_name}"'
    exec_or_bail(cmd, verbose=verbose)
    print("")


def exec_on_guest(cmd: str, *, verbose: bool = False, bail_on_error: bool = True) -> int:
    if verbose:
        print_info(f"Executing command '{cmd}' ...\n")

    code = subprocess.call(["vagrant", "ssh", "-c", cmd])

    if bail_on_error and code != 0:
        bail()

    return code
