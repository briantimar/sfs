"""Module for handling indivdual TCP sockets."""
import socket

class TCPModule:
    """One half of a TCP connection."""

    def __init__(self, port_number=None, rec_buf_size=1024, timeout=5):
        """port_number: if provided, will attempt to bind to this port number.
        rec_buf_size: the size of the receiving buffer used in recv() calls, in bytes.
        timeout = default timeout for all socket operations, in seconds"""
        self.port_number = port_number
        self.rec_buf_size = rec_buf_size
        self.timeout = timeout

        self._id = "" if self.port_number is None else str(self.port_number)

        #local read buffer, currently with no size limit
        self._read_buffer = bytearray(b'')
        # current bytes chunk
        self._chunk = b''

    def log(self, s):
        print(s)

    def _flush_read(self):
        """Flush the read buffer."""
        self._read_buffer = bytearray(b'')

    def _fill_buffer(self, connection, n):
        """Fill the read buffer from the given connection, until it contains at least n bytes.
            """
        while len(self._read_buffer) < n:
            self._read_buffer += connection.recv(self.rec_buf_size)

    def _read(self, connection, n):
        """Read the next n bytes from the given connection"""
        self._fill_buffer(connection, n)
        self._chunk = bytes(self._read_buffer[:n])
        self._read_buffer = self._read_buffer[n:]
        return self._chunk
