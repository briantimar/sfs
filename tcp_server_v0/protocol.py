"""A standard protocol for sending TCP messages."""
from math import log10, ceil
#max length of any single message, in bytes
MAX_LENGTH_LOG10 = 9
PREFIX_SIZE = MAX_LENGTH_LOG10 + 1

def encode_length(n):
    """Encodes integer length into fixed-size  string."""
    if n < 2:
        nd = 1
    else:
        nd = ceil(log10(n))
    if nd >= MAX_LENGTH_LOG10:
        raise ValueError(f"Message size of {n} bytes is too large.")
    return "0" * (MAX_LENGTH_LOG10 - nd) + str(n)

def decode_length(bytes_prefix):
    """Returns integer corresponding to the given bytes prefix, eg 0005: -> 5"""
    assert len(bytes_prefix) == PREFIX_SIZE
    return int(bytes_prefix[:-1])

def len_encode(message):
    """Encodes a bytes message, by prepending the length of the message."""
    return bytes(encode_length(len(message)), "ascii") + b":" + message

def encode(message):
    return len_encode(message)