from abc import ABC, abstractmethod
import pickle
from collections import UserList
from re import fullmatch


class AbstractAddressBook(ABC):
    
    @abstractmethod
    def add_record(self, record):
        pass

    @abstractmethod
    def delete_record(self, record):
        pass

    @abstractmethod
    def find_record(self, contact_name):
        pass

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_data(self):
        pass


class AddressBook(UserList, AbstractAddressBook):
    
    def add_record(self, record):
        self.data.append(record)

    def delete_record(self, record):
        self.data.remove(record)

    def find_record(self, contact_name):
        for record in self.data:
            if record.name.value == contact_name:
                return record

        raise ValueError(f'Contact name "{contact_name}" doesn\'t exist.')

    def read_data(self):
        try:
            with open("address_book_data.bin", "rb") as file:
                contacts = pickle.load(file)
        except FileNotFoundError as e:
            contacts = self
        except EOFError as e:
            contacts = self
        finally:
            return contacts

    def write_data(self):
        with open("address_book_data.bin", "wb") as file:
            pickle.dump(self, file)


class AbstractRecord(ABC):

    @abstractmethod
    def add_phone(self, phone):
        pass

    @abstractmethod
    def delete_phone(self, phone):
        pass

    @abstractmethod
    def edit_email(self, new_email):
        pass

    @abstractmethod
    def edit_birth_date(self, new_birth_date):
        pass


class Record(AbstractRecord):

    def __init__(self, name, phone, email, birthday):
        self.name = name
        self.phones = [phone]
        self.email = email
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        for phone_object in self.phones:
            if phone_object.value == phone:
                self.phones.remove(phone_object)
                break
        else:
            print(f'Phone number "{phone}" doesn\'t exist.')

    def edit_email(self, new_email):
        self.email = new_email

    def edit_birth_date(self, new_birth_date):
        self.birthday = new_birth_date


class Field:

    def __init__(self, value):
        if 1 <= len(value) <= 50:
            self.value = value
        else:
            raise ValueError("Title length must be between 1 and 50 characters.")

    def __repr__(self):
        return str(self.value)

    def __str__(self):
        return str(self.value)


class Birthday(Field):

    def __init__(self, value):
        if value == "" or fullmatch(
            r"(0[1-9]|[12][0-9]|3[01])/(0[1-9]|[1][12])/(19|20)\d\d", value
        ):
            self.value = value
        else:
            raise ValueError(
                'Enter the birthday date according to the specified template "XX/XX/XXXX".'
            )


class Email(Field):

    def __init__(self, value):
        if value == "" or fullmatch(r"[\w.-]+@([\w]+\.)+[\w-]{2,4}", value):
            self.value = value
        else:
            raise ValueError(
                'Enter the email according to the specified template "X@X.X".'
            )


class Name(Field):
    pass


class Phone(Field):

    def __init__(self, value):
        if fullmatch(r"\+\d{3}\(\d{2}\)\d{3}-\d{2}-\d{2}", value):
            self.value = value
        else:
            raise ValueError(
                'Enter the phone number according to the specified template "+XXX(XX)XXX-XX-XX".'
            )
