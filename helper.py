from termcolor import colored
from pyfiglet import Figlet


def big_print(text):
    print(colored(Figlet(font="slant").renderText(text), "cyan"))


def colored_print(text, color="cyan"):
    try:
        print(colored(text, color))
    except:
        print(text)


def get_choice(options):
    for i, opt in enumerate(options, 1):
        print(f"{i}. {opt}")
    return input("Enter choice: ")


def select_enum(enum_cls):
    print(f"\nSelect {enum_cls.__name__}:")
    opts = [e.value for e in enum_cls if e.name != "pending"]
    for i, opt in enumerate(opts, 1):
        print(f"{i}. {opt}")
    sel = input("Choice (enter to skip): ")
    return (
        opts[int(sel) - 1]
        if sel.isdigit() and 1 <= int(sel) <= len(opts)
        else "pending"
    )


def calculate_gpa(marks):
    if marks >= 90:
        return 4.00
    elif marks >= 85:
        return 3.75
    elif marks >= 80:
        return 3.50
    elif marks >= 75:
        return 3.25
    elif marks >= 70:
        return 3.00
    elif marks >= 65:
        return 2.75
    elif marks >= 60:
        return 2.50
    elif marks >= 50:
        return 2.25
    return 0.00
