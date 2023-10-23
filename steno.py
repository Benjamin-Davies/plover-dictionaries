"""
Functions to validate and sort steno dictionaries.
"""

STENO_ORDER = "#STKPWHRAO*EUFRPBLGTSDZ"
NUMBER_KEYS = "OSTPHAFPLT"
MIDDLE = STENO_ORDER.index("*")


def process_numbers(stroke: str) -> str:
    """
    Replaces numbers with the corresponding steno characters.
    """
    if "/" in stroke:
        return "/".join(map(process_numbers, stroke.split("/")))

    if stroke[0] == "#":
        is_number = True
        stroke = stroke[1:]
    else:
        is_number = False

    for index, char in enumerate(stroke):
        if char.isdigit():
            stroke = stroke[:index] + NUMBER_KEYS[int(char)] + stroke[index + 1 :]
            is_number = True

    if is_number:
        stroke = "#" + stroke

    return stroke


def steno_indices(key: str) -> list[int]:
    """
    Returns a list of indices for the given steno stroke.
    """
    key = process_numbers(key)
    min_index = 0
    indices = []
    for char in key:
        if char == "-":
            # Skip to the middle and don't count this char.
            min_index = MIDDLE + 1
            continue

        if char == "/":
            # Reset the minimum index for the next stroke.
            min_index = 0

        index = STENO_ORDER.find(char, min_index)
        indices.append(index)
        if index != -1:
            min_index = index + 1

    return indices


def is_steno_stroke(stroke: str) -> bool:
    """
    Returns True if the stroke is in steno order, False otherwise.
    """
    indices = steno_indices(stroke)
    return all((index != -1 for index in indices))


def validate_dictionary(dictionary: dict[str, str]):
    """
    Validates the keys of the given steno dictionary.

    >>> validate_dictionary({"H-L": "hello", "WORLD": "world"})
    >>> validate_dictionary({"HI": "hello", "WOLRD": "world"})
    Invalid key: HI
    Invalid key: WOLRD
    """
    for key in dictionary.keys():
        if not all((is_steno_stroke(stroke) for stroke in key.split("/"))):
            print(f"Invalid key: {key}")


def sort_dictionary(dictionary: dict[str, str]) -> dict[str, str]:
    """
    Sorts the given steno dictionary into steno order.
    """
    return dict(sorted(dictionary.items(), key=lambda item: steno_indices(item[0])))
