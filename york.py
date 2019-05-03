#!/usr/bin/env python3
"""
york.py

Decrypts Elma and Nathaniel York's private messages.

(See _The Fated Sky_ by Mary Robinette Kowal, starting on p. 194.)

Usage:

    york KEY < CIPHERTEXT

Replace KEY with the Ceasar cipher text key found in the book (not the numbers
that index Kipling -- maybe a future version will support that).

Replace CIPHERTEXT with the encrypted message text.
"""

import contextlib
import string
import sys


def join(func):
    """Decorator so a returned sequence of characters is joined to a string."""
    return lambda *args: ''.join(func(*args))


def die(message):
    """Exits reporting failure with the specified error message."""
    print(f'{sys.argv[0]}: error: {message}')
    sys.exit(1)


def get_key():
    """Gets the key from the command line."""
    try:
        _, key = sys.argv  # pylint: disable=unbalanced-tuple-unpacking
        return key
    except ValueError:
        die(f'too {"few" if len(sys.argv) < 2 else "many"} arguments')


@join
def get_substitution_alphabet():
    """Gets the key and converts it to a substitution alphabet."""
    alphabet = []

    for ch in get_key().lower() + string.ascii_lowercase:
        if ch not in alphabet:
            alphabet.append(ch)

    if len(alphabet) != len(string.ascii_lowercase):
        die('key must consist solely of ASCII letters')

    return alphabet


@join
def decrypt(alphabet, ciphertext):
    """Uses the substitution alphabet to decrypt the ciphertext."""
    for ch in ciphertext:
        # Try to substitute for a lower-case letter.
        with contextlib.suppress(ValueError):
            yield string.ascii_lowercase[alphabet.index(ch)]
            continue

        # Try to substitute for an upper-case letter.
        with contextlib.suppress(ValueError):
            yield string.ascii_uppercase[alphabet.index(ch.lower())].upper()
            continue

        # Pass unsubstitutable letters through unchanged.
        yield ch


def read_ciphertext():
    """Reads to the end of stdin, reporting if there are errors."""
    try:
        return sys.stdin.read()
    except IOError as e:
        die(f"can't read ciphertext: {e.strerror}")


def run():
    """Decrypts stdin with the Ceasear cipher key given on the command line."""
    alphabet = get_substitution_alphabet()
    print(f'Substitution alphabet:  {alphabet}', file=sys.stderr)
    print(file=sys.stderr)

    print(decrypt(alphabet, read_ciphertext()))


if __name__ == '__main__':
    run()
