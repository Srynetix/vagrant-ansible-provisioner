import json
from argparse import ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import Any, Dict, Optional

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import exec_or_bail, print_info
from vagrant_ansible_provisioner.vagrant import (
    generate_box_manifest,
    reset_authorized_keys,
)


class PackageBoxCommand(Command):
    name = "package-box"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        vm_name: str = args.vm_name
        box_name: str = args.box_name
        box_path: str = args.box_path
        box_description: str = args.box_description
        box_version: str = args.box_version
        box_engine: str = args.box_engine
        box_url: str = args.box_url

        verbosity = config.verbosity.getv()
        self.prepare_box(verbosity)
        self.build_box(
            vm_name=vm_name,
            box_name=box_name,
            box_path=box_path,
            box_description=box_description,
            box_version=box_version,
            box_engine=box_engine,
            box_url=box_url,
            verbosity=verbosity,
        )
        return 0

    def prepare_box(self, verbosity: int) -> None:
        # Prior to generating the box, you have to do some things, like adding the Vagrant insecure public key
        reset_authorized_keys(verbose=verbosity > 0)

    def build_box(
        self,
        *,
        verbosity: int,
        vm_name: str,
        box_name: str,
        box_path: str,
        box_description: str,
        box_version: str,
        box_engine: str,
        box_url: Optional[str] = None,
    ) -> None:
        verbose = verbosity > 0
        exec_or_bail("vagrant halt", verbose=verbose)
        exec_or_bail(f"vagrant package {vm_name} --output {box_path}", verbose=verbose)

        manifest = generate_box_manifest(
            name=box_name,
            description=box_description,
            version=box_version,
            path=box_path,
            engine=box_engine,
            url=box_url,
        )
        self.write_manifest(manifest, str(Path(box_path).with_suffix(".json")))

    def write_manifest(self, manifest: Dict[str, Any], path: str) -> None:
        with open(path, mode="w") as f:
            json.dump(manifest, f, indent=4)
        print_info(f"Manifest written at path '{path}'")

    @staticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        package_box_cmd = subp.add_parser("package-box", help="create a Vagrant box")
        package_box_cmd.add_argument("vm_name", help="VM name")
        package_box_cmd.add_argument("box_path", help="box path")
        package_box_cmd.add_argument("--box-name", required=True, help="box name")
        package_box_cmd.add_argument("--box-description", required=True, help="box description")
        package_box_cmd.add_argument("--box-version", required=True, help="box version")
        package_box_cmd.add_argument("--box-engine", help="box engine (optional)", default="virtualbox")
        package_box_cmd.add_argument("--box-url", help="box URL (optional)", default=None)
