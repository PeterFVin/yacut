from random import choice
from string import ascii_letters, digits


def get_unique_short_id():
    return ''.join(choice(ascii_letters + digits) for i in range(6))
