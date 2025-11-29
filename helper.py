from pyfiglet import Figlet
from termcolor import colored


def printChoice(choices: list):
    for x, choice in enumerate(choices):
        print(f"{x+1}. {choice}")
    return input("Enter choice: ")


def print_enum_choice(enum_cls, prompt):
    print(f"\n--- Select {prompt} ---")
    options = [e.value for e in enum_cls if e.name != "pending"]
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")

    while True:
        sel = input("Select number (or enter to skip): ")
        if not sel:
            return "pending"
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return options[int(sel) - 1]
        print("Invalid selection, try again.")


def prettyPrint(text: str, color: str = "cyan"):
    try:
        f = Figlet(font="slant")
        text = f.renderText(text)
        print(colored(text, color, attrs=["bold"]))
    except:
        print(text)


def coloredPrint(text: str, color: str = "cyan"):
    try:
        print(colored(text, color=color, attrs=["bold"]))
    except:
        print(text)
