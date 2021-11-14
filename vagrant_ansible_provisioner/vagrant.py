import hashlib
import os
from typing import Any, Dict, Optional

from .utils import exec_or_bail, print_info

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
