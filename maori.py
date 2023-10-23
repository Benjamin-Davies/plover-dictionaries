"""
Functions for parsing Māori words into phonemes, and then converting those into steno strokes.
"""

import re
from typing import Literal

NON_ASCII_LETTER = re.compile(r"[^a-z]+")

# Search diphthongs first, then single letters.
CONSONANT_CHORDS = {
    "ng": "TKPW",
    "wh": "WH",
    "h": "H",
    "k": "K",
    "m": "PH",
    "n": "TPH",
    "p": "P",
    "r": "R",
    "t": "T",
    "w": "W",
}
VOWEL_CHORDS = {
    "ae": "AE",
    "ai": "AEU",
    "ao": "AO",
    "au": "AU",
    "ou": "OU",
    "a": "A",
    "e": "E",
    "i": "EU",
    "o": "O",
    "u": "U",
}

CONSONANTS = list(CONSONANT_CHORDS.keys())
VOWELS = list(VOWEL_CHORDS.keys())

SUFFIX = "GSD"


def normalise(phrase: str) -> str:
    """
    Replaces all characters with ASCII letters or spaces.

    >>> normalise("Te Ahi-kai-kōura-a-Tama-ki-te-rangi")
    'te ahi kai koura a tama ki te rangi'
    >>> normalise("WHĀNGAREI")
    'whangarei'
    """
    phrase = (
        phrase.lower()
        .replace("ā", "a")
        .replace("ē", "e")
        .replace("ī", "i")
        .replace("ō", "o")
        .replace("ū", "u")
    )
    phrase = NON_ASCII_LETTER.sub(" ", phrase)
    return phrase


def split_phonemes(phrase: str) -> list[tuple[Literal["C", "V"], str]]:
    """
    Splits a Māori phrase into consonants ("C") and vowels ("V").

    >>> split_phonemes("Whare kai")
    [('C', 'wh'), ('V', 'a'), ('C', 'r'), ('V', 'e'), ('C', 'k'), ('V', 'ai')]
    >>> split_phonemes("WHĀNGAREI")
    [('C', 'wh'), ('V', 'a'), ('C', 'ng'), ('V', 'a'), ('C', 'r'), ('V', 'e'), ('V', 'i')]
    """
    phrase = phrase.strip()
    phrase = normalise(phrase)

    phonemes: list[tuple[Literal["C", "V"], str]] = []
    while len(phrase) > 0:
        phrase = phrase.lstrip()
        identified = False

        for consonant in CONSONANTS:
            if phrase.startswith(consonant):
                phonemes.append(("C", consonant))
                phrase = phrase[len(consonant) :]
                identified = True
                break

        for vowel in VOWELS:
            if phrase.startswith(vowel):
                phonemes.append(("V", vowel))
                phrase = phrase[len(vowel) :]
                identified = True
                break

        if not identified:
            raise NotImplementedError("Unknown phoneme: " + phrase)

    return phonemes


def steno_key(phrase: str) -> str:
    """
    Generates the key for the given Māori phrase in a Plover dictionary.

    >>> steno_key("Whare kai")
    'WHAGSD/REGSD/KAEUGSD'
    >>> steno_key("WHĀNGAREI")
    'WHAGSD/TKPWAGSD/REGSD/EUGSD'
    """
    strokes = []

    phonemes = iter(split_phonemes(phrase))
    try:
        while True:
            ty1, ph1 = next(phonemes)
            if ty1 == "C":
                consonant = CONSONANT_CHORDS[ph1]

                ty2, ph2 = next(phonemes, (None, None))
                # Māori sylables always take the form CV or V.
                assert ty2 == "V"
                vowel = VOWEL_CHORDS[ph2]
            else:
                consonant = ""
                vowel = VOWEL_CHORDS[ph1]

            strokes.append(consonant + vowel + SUFFIX)
    except StopIteration:
        pass

    return "/".join(strokes)
