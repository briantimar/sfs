"""Module for parsing and forming HTTP messages.
    """

HTTP_VERSION = b'HTTP/1.1'
CRLF = b'\r\n'
SP = b' '

def ascii_bytes(string):
    """Convert a python string into sequence of ascii bytes. 
        DOES ABSOLUTELY NO RECOVERY WHATSOEVER so this conversion had better be possible..."""
    return bytes(string, "ascii")

def get_status_and_reason(int_code):
    """Returns tuple of bytes holding code and reason phrase for the given integer code."""
    codes = {200: b'OK'}
    if int_code not in codes:
        raise ValueError(f"Invalid code: {int_code}")
    return bytes(str(int_code), 'ascii'), codes[int_code]

def build_message(start_line, headers, body=b''):
    """Constructs an HTTP message from the provided start line, headers, and body, and returns the corresponding
    bytes object.
        start_line: bytes, either a request or status line
        headers: iterable of header lines (not including the final newline)
        body: bytes representing the message body. This is allowed to be empty.
        """
    msg = bytearray(start_line)
    for header in headers:
        msg += header + CRLF
    msg += CRLF
    msg += body
    return bytes(msg)

def build_status_line(status_code, reason_phrase):
    """ Returns a status line.
        status_code : bytes a valid status code.
        reason_phrase: bytes, textual description of the status.
        returns: bytes.
        """
    return SP.join((HTTP_VERSION, status_code, reason_phrase)) + CRLF

def get_status_line(int_code):
    """ Returns bytes status line corresponding to the given integer code."""
    return build_status_line(*get_status_and_reason(int_code))

def build_header_line(field_name, field_value):
    """Build a header line of the form name: value
        field_name: bytes representing a field name
        field_value: bytes representing a field value.
    
        Right now not checking for validity."""
    return field_name + b" : " + field_value

def get_header_lines(header_map):
    """Given a dict with string field:value maps, returns an iterable of bytes header lines.
        Does not check order."""
    return [ build_header_line(ascii_bytes(name), ascii_bytes(value))
                for (name, value) in header_map.items()]

def get_ok_response(body_string=""):
    """Builds a bytes object holding HTTP response with the given body"""
    status_line = get_status_line(200)
    headers = {"Host":"localhost"}
    body = body_string.encode("utf-8")
    return build_message(status_line, get_header_lines(headers), body=body)