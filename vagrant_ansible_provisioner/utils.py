import os
import shlex
import subprocess
import sys
from contextlib import contextmanager
from typing import Any, Dict, Generator, NoReturn, Optional

from termcolor import colored as _colored
from termcolor import cprint as _cprint


def bail() -> NoReturn:
    print_error("Abort.")
    sys.exit(1)


def exec_or_bail(cmd: str, *, verbose: bool = False, env: Optional[Dict[str, Any]] = None) -> None:
    if verbose:
        print_info(f"Executing command '{cmd}' ...\n")

    with using_tmp_envs(env or {}):
        code = subprocess.call(shlex.split(cmd))

    if code != 0:
        bail()


def exec_output(cmd: str, *, verbose: bool = False, env: Optional[Dict[str, Any]] = None) -> bytes:
    if verbose:
        print_info(f"Executing command '{cmd}' ...\n")

    with using_tmp_envs(env or {}):
        return subprocess.check_output(shlex.split(cmd))


def yes_no_prompt(msg: str) -> bool:
    while True:
        choice = input(colored("? {m} (y/n) ".format(m=msg), color="blue"))

        try:
            if choice.lower() == "y":
                return True
            elif choice.lower() == "n":
                return False
        except BaseException:
            pass


def clear_screen() -> None:
    subprocess.call(["cls"] if os.name == "nt" else ["clear"], shell=True)


def exec_and_quit(msg: str, cmd: str, *, verbose: bool = False, env: Optional[Dict[str, Any]] = None) -> None:
    print_info(msg)
    exec_or_bail(cmd, verbose=verbose, env=env)

    cprint("✅ Success.", color="green")
    sys.exit(0)


def print_step(txt: str) -> None:
    print("")
    cprint("=" * (len(txt) + 5), color="blue")
    cprint(f" 🚀 {txt}", color="blue")
    cprint("=" * (len(txt) + 5), color="blue")
    print("")


def print_task(txt: str, newline: bool = False) -> None:
    print("")
    cprint(f"📜 {txt} ", color="blue", end="\n" if newline else "")


def cprint(text: str, color: str, **kwargs: Any) -> None:
    _cprint(text, color=color, **kwargs)


def colored(text: str, color: str) -> str:
    return _colored(text, color=color)


def print_info(text: str, *, color: str = "blue", prefix: str = "⚙️ ", **kwargs: Any) -> None:
    if len(prefix) > 0:
        text = f"{prefix} {text}"
    _cprint(text, color=color, **kwargs)


def print_error(text: str, *, color: str = "red", prefix: str = "❌", **kwargs: Any) -> None:
    print_info(text, color=color, prefix=prefix, file=sys.stderr)


def print_warn(text: str, *, color: str = "yellow", prefix: str = "⚠️ ", **kwargs: Any) -> None:
    print_info(text, color=color, prefix=prefix)


@contextmanager
def using_tmp_envs(env: Dict[str, Any]) -> Generator:
    prev_values = {k: os.environ.get(k) for k in env.keys()}

    for k, v in env.items():
        os.environ[k] = str(v)

    yield

    for k, v in prev_values.items():
        if v is None:
            os.environ.pop(k)
        else:
            os.environ[k] = str(v)
