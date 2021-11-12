import os
import sys

from termcolor import colored as _colored
from termcolor import cprint as _cprint


def bail():
    cprint("❌ Abort.", color="red", file=sys.stderr)
    sys.exit(1)


def exec_or_bail(cmd: str, *, verbose: bool = False):
    if verbose:
        cprint(f"⚙️  Executing command '{cmd}' ...\n", color="blue")
    code = os.system(cmd)
    if code != 0:
        bail()


def yes_no_prompt(msg: str) -> bool:
    while True:
        choice = input(colored("❔ {m} (y/n) ".format(m=msg), color="blue"))

        try:
            if choice.lower() == "y":
                return True
            elif choice.lower() == "n":
                return False
        except BaseException:
            pass


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def exec_and_quit(msg: str, cmd: str, *, verbose: bool = False):
    print(msg)
    exec_or_bail(cmd, verbose=verbose)

    cprint("✅ Success.", color="green")
    sys.exit(0)


def print_step(txt: str):
    print("")
    cprint("=" * (len(txt) + 5), color="blue")
    cprint(f" 🚀 {txt}", color="blue")
    cprint("=" * (len(txt) + 5), color="blue")
    print("")


def print_task(txt: str, newline: bool = False):
    print("")
    cprint(f"📜 {txt} ", color="blue", end="\n" if newline else "")


def cprint(text: str, color: str, **kwargs):
    _cprint(text, color=color, **kwargs)


def colored(text: str, color: str):
    return _colored(text, color=color)
