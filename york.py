#!/usr/bin/env python3

import contextlib
import string
import sys


def die(message):
    print(f'{sys.argv[0]}: error: {message}')
    sys.exit(1)


def join(func):
    return lambda *args: ''.join(func(*args))


def get_key():
    try:
        _, key = sys.argv
        return key
    except ValueError:
        die(f'too {"few" if len(sys.argv) < 2 else "many"} arguments')


@join
def get_substitution_alphabet():
    alphabet = []

    for ch in get_key().lower() + string.ascii_lowercase:
        if ch not in alphabet:
            alphabet.append(ch)

    if len(alphabet) != len(string.ascii_lowercase):
        die('key must consist solely of ASCII letters')

    return alphabet


@join
def decrypt(alphabet, ciphertext):
    for ch in ciphertext:
        # Try to substitute for a lower-case letter.
        with contextlib.suppress(ValueError):
            return string.ascii_lowercase[alphabet.index(ch)]

        # Try to substitute for an upper-case letter.
        with contextlib.suppress(ValueError):
            return string.ascii_uppercase[alphabet.index(ch.lower())].upper()

        # Pass unsubstitutable letters through unchanged.
        return ch


def read_ciphertext(path):
    try:
        with open(path) as file:
            return file.read()
    except IOError as e:
        die(f'{e.filename}: {e.strerror}')
