
import sys

print(sys.path)
from address_book_main import main_address_book
from file_sorter import main_sorter
from note_book_main import main_note_book

import inquirer


questions = [
    inquirer.List(
        "option",
        message="B0tHe1Per",
        choices=[
            "Address book",
            "Note book",
            "Sorter",
            "Exit",
        ],
    )
]


def main():
    while True:
        handler = get_handler()

        if handler == "Exit":
            break

        handler()


def get_handler():
    command = inquirer.prompt(questions)
    return COMMANDS[command["option"]]


COMMANDS = {
    "Address book": main_address_book,
    "Note book": main_note_book,
    "Sorter": main_sorter,
    "Exit": "Exit",
}

main()
