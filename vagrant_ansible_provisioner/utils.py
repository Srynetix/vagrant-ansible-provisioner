import os
import sys


def bail():
    print("")
    print("=> Exiting")
    print("")
    sys.exit(1)


def exec_or_bail(cmd: str):
    code = os.system(cmd)
    if code != 0:
        bail()


def yes_no_prompt(msg: str) -> bool:
    while True:
        choice = input("/!\\ {m} (y/n) ".format(m=msg))

        try:
            if choice.lower() == "y":
                return True
            elif choice.lower() == "n":
                return False
        except BaseException:
            pass


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def exec_and_quit(msg: str, cmd: str):
    print(msg)
    exec_or_bail(cmd)

    print("")
    print("=> Success")
    print("")


def print_step(txt: str):
    print("")
    print("=" * (len(txt) + 2))
    print(f" {txt}")
    print("=" * (len(txt) + 2))
    print("")


def print_task(txt: str, newline: bool = False):
    print("")
    print(f"> {txt} ", end="\n" if newline else "")
