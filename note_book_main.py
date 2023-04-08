from note_book_classes import *
import inquirer


NOTES = NoteBook().read_data()

questions = [
    inquirer.List("option",
                  message="Note Book Menu",
                  choices=[
                      'Add note',
                      'Read note',
                      'Edit note',
                      'Delete note',
                      'Display all notes',
                      'Add tag',
                      'Edit tag',
                      'Search',
                      'Search by tags',
                      'Quit',
                  ])
]


def main_note_book():
    while True:
        handler = get_handler()

        if handler == "Quit":
            break

        handler()
        input("Press \"Enter\" to go to the menu.")
        NOTES.write_data()

# Decorator for exception handling
def input_error(function):

    def wrapper():
        try:
            result = function()
            return result
        except ValueError as e:
            print(e)
    
    return wrapper
           
# Carrying  
def get_handler():
    command = inquirer.prompt(questions)
    return COMMANDS[command["option"]]

# Adds a note
@input_error
def add_note():
    title = Title(input("Enter title: "))
    body = Body(input("Enter note: "))
    row_tags = input("Enter tags separated by space: ")
    tags = list(map(lambda x: Tag(x), row_tags.split()))
    note = Note(title, body, tags)
    NOTES.add_note(note)

# Adds tags to the note
@input_error
def add_tags():
    note = NOTES.find_note(input("Enter title: "))
    note.add_tags(input("Enter tags separated by space: "))

# Deletes the note
@input_error
def delete_note():
    note = NOTES.find_note(input("Enter title: "))
    NOTES.delete_note(note)

# Displays the titles of all existing notes
def display_all_notes(notes=NOTES):
    if notes:
        for note in notes:
            print(note)
    else:
        print("You have no notes.")

# Editing the body of the note
@input_error
def edit_note():
    note = NOTES.find_note(input("Enter title: "))
    new_body = Body(input("Enter note: "))
    note.edit_note(new_body)

# Editing the tags of the note
@input_error
def edit_tags():
    note = NOTES.find_note(input("Enter title: "))
    row_new_tags = input("Enter tags separated by space: ")
    new_tags = list(map(lambda x: Tag(x), row_new_tags.split()))
    note.edit_tags(new_tags)

# Displays the body and tags of the note
@input_error
def read_note():
    note = NOTES.find_note(input("Enter title: "))
    note.read_note()

# Searches notes by the specified string
def search():
    string = input("Enter string: ")
    notes_list = []

    for note in NOTES:
        if string in note.title.value or string in note.body.value:
            notes_list.append(note)
        
    display_all_notes(notes_list)

# Searches notes by tag
def search_by_tag():
    tag = input("Enter tag: ")
    notes_list = []

    for note in NOTES:
        tags = list(map(lambda x: x.value, note.tags))

        if tag in tags:
            notes_list.append(note)
        
    display_all_notes(notes_list)


COMMANDS = {
    'Add note': add_note,
    'Read note': read_note,
    'Edit note': edit_note,
    'Delete note': delete_note,
    'Display all notes': display_all_notes,
    'Add tag': add_tags,
    'Edit tag': edit_tags,
    'Search': search,
    'Search by tags': search_by_tag,
    "Quit": "Quit",
}


if __name__ == '__main__':
    main_note_book()

