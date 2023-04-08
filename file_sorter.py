import os
from pathlib import Path
import shutil


FILE_TYPES = {
    "images": (".jpeg", ".png", ".jpg", ".svg"),
    "documents": (".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"),
    "audio": (".mp3", ".ogg", ".wav", ".amr"),
    "video": (".avi", ".mp4", ".mov", ".mkv"),
    "archives": (".zip", ".gz", ".tar"),
}


def main_sorter():
    path = input("Enter directory path: ")

    if os.path.exists(path):
        create_folders(path)
        rename(path)
        sort_directory(path)
        delete_empty_directories(path)
        print("Your folder is sorted.")
    else:
        print("Path doesn't exist")


def create_folders(path):
    for key in FILE_TYPES:
        new_directory_path = os.path.join(path, key)
        os.makedirs(new_directory_path, exist_ok=True)


def delete_empty_directories(path):
    path = Path(path)

    for elem in path.iterdir():
        if elem.is_dir() and not elem.name in FILE_TYPES.keys():
            delete_empty_directories(elem)
            try:
                elem.rmdir()
            except OSError:
                continue


def normalize(file_name):
    cyrirllic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    latin_symbols = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "e",
        "j",
        "z",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "ts",
        "ch",
        "sh",
        "sch",
        "",
        "y",
        "",
        "e",
        "yu",
        "ya",
        "je",
        "i",
        "ji",
        "g",
    )

    trans = {}

    for c, t in zip(cyrirllic_symbols, latin_symbols):
        trans[ord(c)] = t
        trans[ord(c.upper())] = t.capitalize()

    new_file_name = file_name.translate(trans)

    for symbol in new_file_name:

        if (
            not ord(symbol) in range(48, 58)
            and not ord(symbol) in range(65, 91)
            and not ord(symbol) in range(97, 122)
        ):
            new_file_name = new_file_name.replace(symbol, "_")

    return new_file_name


def rename(path):
    path = Path(path)

    for element_path in path.iterdir():
        if element_path.is_dir():
            rename(element_path)
            directory_name = element_path.name
            new_directory_name = normalize(directory_name)
            new_element_path = element_path.parent / new_directory_name

            if not new_element_path.exists():
                element_path.rename(new_element_path)
        else:
            file_name = element_path.stem
            new_file_name = normalize(file_name) + element_path.suffix
            new_element_path = element_path.parent / new_file_name

            if not new_element_path.exists():
                element_path.rename(new_element_path)


def sort_directory(path):
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            name, extension = os.path.splitext(filename)

            if extension in FILE_TYPES["images"] and os.path.join(
                path, "archives"
            ) not in os.path.join(dirpath, filename):
                if not os.path.exists(os.path.join(path, "images", filename)):
                    shutil.move(
                        os.path.join(dirpath, filename),
                        os.path.join(path, "images", filename),
                    )
            elif extension in FILE_TYPES["documents"] and os.path.join(
                path, "archives"
            ) not in os.path.join(dirpath, filename):
                if not os.path.exists(os.path.join(path, "documents", filename)):
                    shutil.move(
                        os.path.join(dirpath, filename),
                        os.path.join(path, "documents", filename),
                    )
            elif extension in FILE_TYPES["audio"] and os.path.join(
                path, "archives"
            ) not in os.path.join(dirpath, filename):
                if not os.path.exists(os.path.join(path, "audio", filename)):
                    shutil.move(
                        os.path.join(dirpath, filename),
                        os.path.join(path, "audio", filename),
                    )
            elif extension in FILE_TYPES["video"] and os.path.join(
                path, "archives"
            ) not in os.path.join(dirpath, filename):
                if not os.path.exists(os.path.join(path, "video", filename)):
                    shutil.move(
                        os.path.join(dirpath, filename),
                        os.path.join(path, "video", filename),
                    )
            elif extension in FILE_TYPES["archives"]:
                shutil.unpack_archive(
                    os.path.join(dirpath, filename),
                    os.path.join(path, "archives", name),
                )
                os.unlink(os.path.join(dirpath, filename))


if __name__ == "__main__":
    main_sorter()
