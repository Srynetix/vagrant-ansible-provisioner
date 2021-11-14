import shlex
import subprocess
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import List, NamedTuple

from vagrant_ansible_provisioner.command import Command
from vagrant_ansible_provisioner.config import EnvironmentConfig
from vagrant_ansible_provisioner.utils import cprint, exec_output


class SshConfig(NamedTuple):
    hostname: str
    user: str
    port: int
    identity_file: str


class PortForwardCommand(Command):
    name = "port-forward"

    def execute(self, args: Namespace, config: EnvironmentConfig) -> int:
        ports: List[int] = args.port
        verbosity = config.verbosity.getv()
        ssh_config = self.extract_ssh_config(verbosity)

        rules = " ".join(f"-L *:{p}:{ssh_config.hostname}:{p}" for p in ports)
        cmd = (
            f"ssh {rules} -i {ssh_config.identity_file} {ssh_config.user}@{ssh_config.hostname} -p {ssh_config.port} -N"
        )

        print(f" * Forwarding ports {', '.join(str(p) for p in ports)} ...")
        print("   Type CTRL+C to stop.")
        if verbosity > 0:
            cprint(f"Executing command '{cmd}'", color="blue")

        try:
            subprocess.call(shlex.split(cmd))
        except KeyboardInterrupt:
            print("Quitting.")
        return 0

    def extract_ssh_config(self, verbosity: int) -> SshConfig:
        output = exec_output("vagrant ssh-config", verbose=verbosity > 0).decode()
        ssh_lines = [line.strip() for line in output.splitlines()]
        hostname = next(line for line in ssh_lines if line.startswith("HostName ")).split(" ")[1]
        user = next(line for line in ssh_lines if line.startswith("User ")).split(" ")[1]
        port = int(next(line for line in ssh_lines if line.startswith("Port ")).split(" ")[1])
        identity_file = next(line for line in ssh_lines if line.startswith("IdentityFile ")).split(" ")[1]

        return SshConfig(hostname=hostname, user=user, port=port, identity_file=identity_file)

    @staticmethod
    def add_arguments(parser: ArgumentParser, subp: _SubParsersAction) -> None:
        cmd = subp.add_parser("port-forward", help="forward ports")
        cmd.add_argument("port", nargs="+", type=int, help="ports to open")
