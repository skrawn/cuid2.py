import binascii
import string
from random import SystemRandom


def string_to_int(string: str) -> int:
    raw_string: bytes = string.encode()
    raw_string = binascii.hexlify(raw_string)

    return int(raw_string, 16)


def base36_encode(number: int) -> str:
    if number < 0:
        raise ValueError('Cannot encode negative integers.')

    encoded_string: str = ''
    alphabet: str = string.digits + string.ascii_lowercase

    while number != 0:
        number, mod = divmod(number, 36)
        encoded_string = alphabet[mod] + encoded_string

    return encoded_string or '0'


def random_letter() -> str:
    alphabet: str = string.digits + string.ascii_lowercase
    generator: SystemRandom = SystemRandom()

    return alphabet[int(generator.random() * len(alphabet))]


def pad_string(string: str, i: int) -> str:
    padding: str = "000000000"

    if len(string) == i:
        return string

    if len(string) < i:
        return padding[0:i-len(string)] + string

    return string[-i:]
