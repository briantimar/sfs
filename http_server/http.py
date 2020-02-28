"""Module for parsing and forming HTTP messages."""

def build_message(start_line, headers, body):
    """Constructs an HTTP message from the provided start line, headers, and body, and returns the corresponding
    bytes object.
        start_line: bytes, either a request or status line
        headers: iterable of header lines (not including the final newline)
        body: bytes representing the message body. This is allowed to be empty.
        """
    msg = bytearray(start_line)
    for header in headers:
        msg += header + b'\r\n'
    msg += body
    return msg