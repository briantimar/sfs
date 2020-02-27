"""A standard protocol for sending TCP messages."""

def len_encode(message):
    """Encodes a bytes message, by prepending the length of the message."""
    return bytes(len(message), "ascii") + ":" + message
