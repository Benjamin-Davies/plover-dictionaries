"""
Generates dictionaries from lists of Māori words.
"""

import json

import maori
import steno


def read_words(filename: str) -> list[str]:
    """
    Reads the lines of a file into a list.
    """
    with open(filename, "r", encoding="utf8") as filename:
        return filename.read().splitlines()


def read_dict(filename: str) -> dict[str, str]:
    """
    Reads a Plover dictionary into a dict.
    """
    with open(filename, "r", encoding="utf8") as file:
        return json.load(file)


def save_dict(filename: str, dictionary: dict[str, str]):
    """
    Saves a Plover dictionary.
    """
    with open(filename, "w", encoding="utf8") as file:
        json.dump(dictionary, file, ensure_ascii=False, indent=0)


if __name__ == "__main__":
    # Regular Māori words.
    maori_words = read_words("input/maori.txt")
    d = {maori.steno_key(word): word for word in maori_words}

    d.update(read_dict("input/maori-briefs.json"))

    steno.validate_dictionary(d)
    d = steno.sort_dictionary(d)

    save_dict("maori.json", d)

    # Māori place names.
    place_names_maori = read_words("input/nz-place-names-maori.txt")
    d = {maori.steno_key(word): word for word in place_names_maori}

    steno.validate_dictionary(d)
    d = steno.sort_dictionary(d)

    save_dict("nz-place-names-maori.json", d)

    # English place names.
    d = read_dict("nz-place-names-english.json")

    steno.validate_dictionary(d)
    d = steno.sort_dictionary(d)

    save_dict("nz-place-names-english.json", d)
