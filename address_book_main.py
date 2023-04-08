from address_book_classes import *
from datetime import date
import inquirer


CONTACTS = AddressBook().read_data()

questions = [inquirer.List("option",
                           message="Address Book Menu",
                           choices=[
                               'Add record',
                               'Delete record',
                               'Add phone',
                               'Delete phone',
                               'Edit email',
                               'Edit date of birth',
                               'Birthdays today',
                               'Display user information',
                               'Display all records',
                               'Search',
                               'Quit',
                           ])
]


def main_address_book():
    while True:
        handler = get_handler()

        if handler == "Quit":
            break

        handler()
        input("Press \"Enter\" to go to the menu.")
        CONTACTS.write_data()

# Decorator for exception handling
def input_error(function):

    def wrapper(*args):
        try:
            result = function(*args)
            return result
        except ValueError as e:
            print(e)
        
    return wrapper

# Carrying  
def get_handler():
    command = inquirer.prompt(questions)
    return COMMANDS[command["option"]]

# Adds a record
@input_error
def add_record():
        name = Name(input("Enter contact name: "))
        phone = Phone(input("Enter phone number: "))
        email = Email(input("Enter email (optional): "))
        birthday = Birthday(input("Enter user date of birth (optional): "))
        record = Record(name, phone, email, birthday)
        CONTACTS.add_record(record)

# Adds a phone number to the record
@input_error
def add_phone():
    record = CONTACTS.find_record(input("Enter contact name: "))
    phone = Phone(input("Enter phone number: "))
    record.add_phone(phone)

# Displays birthday people
@input_error
def birthdays_today():
    today = date.today()
    record_list = []

    for record in CONTACTS:
        if not record.birthday.value:
            continue

        day, month, year = record.birthday.value.split('/')

        if today.day == int(day) and today.month == int(month):
            record_list.append(record)
        
    display_records(record_list)    

# Deletes the phone number in the record
@input_error
def delete_phone():
    record = CONTACTS.find_record(input("Enter contact name: "))
    phone = input("Enter phone number: ")
    record.delete_phone(phone)

# Deletes the record
@input_error
def delete_record():
    record = CONTACTS.find_record(input("Enter contact name: "))
    CONTACTS.delete_record(record)

# Displays all existing records
def display_records(records=CONTACTS):
    if records:
        for record in records:
            print(record.name, record.phones, record.email, record.birthday)
    else:
        print("You have no records.")

# Displays the record's contact information
@input_error
def display_user_information():
    record = CONTACTS.find_record(input("Enter contact name: "))
    print(record.name, record.phones, record.email, record.birthday)

# Editing the email of the record
@input_error
def edit_email():
    record = CONTACTS.find_record(input("Enter contact name: "))
    new_email = Email(input("Enter user email (optional): "))
    record.edit_email(new_email)

# Editing the date of the birth of the record
@input_error
def edit_birth_date():
    record = CONTACTS.find_record(input("Enter contact name: "))
    new_birth_date = Birthday(input("Enter user date of birth (optional): "))
    record.edit_birth_date(new_birth_date)

# Search records by the specified string
def search():
    string = input("Enter string: ")
    record_list = []

    for record in CONTACTS:
        phones_value = list(map(lambda phone: phone.value, record.phones))
        record_data = record.name.value + ''.join(phones_value) + record.email.value
        if string and string in record_data:
            record_list.append(record)

    display_records(record_list)


COMMANDS = {
    'Add record': add_record,
    'Delete record': delete_record,
    'Add phone': add_phone,
    'Delete phone': delete_phone,
    'Edit email': edit_email,
    'Edit date of birth': edit_birth_date,
    'Birthdays today': birthdays_today,
    'Display user information': display_user_information, 
    'Display all records': display_records,
    'Search': search,
    'Quit': 'Quit',
}


if __name__ == '__main__':
    main_address_book()