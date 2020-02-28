"""Module for handling indivdual TCP sockets."""
import socket
import select

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
        self._chunk = bytes(self._read_buffer)
        self._read_buffer = bytearray(b'')
        return self._chunk

    def _read(self, connection, n):
        """ Read at most n bytes directly from the connection. Possibly blocking. """
        try:
            return connection.recv(n)
        except socket.timeout:
            return b''
        except socket.error:
            self.log("No data!")
            return b''

    def read_all(self, connection):
        """ Read from a connection until the bytestream dries up.
            Sets the connection to non-blocking mode, and then repeatedly reads from it until a socket.error is raised, 
            which happens when the buffer is empty.
            this is a bit fragile, in the sense that part of a message might be delayed, in which case it'll return
            immediately without seeing the rest. 
            Does not close the connection.

            Returns: bytes object.
            
            """
        connection.setblocking(0)
        data = self._read(connection, self.rec_buf_size)
        while len(data) > 0:
            self._read_buffer += data
            data = self._read(connection, self.rec_buf_size)
        self._flush_read()
        return self._chunk
        

