""" A toy server using python's sockets module - just to demonstrate how to use the TCP api"""
import logging
import socket
import argparse
from protocol import PREFIX_SIZE, decode_length, encode

class TCPModule:
    """One half of a TCP connection."""

    def __init__(self, port_number=None, rec_buf_size=1024):
        """port_number: if provided, will attempt to bind to this port number.
        rec_buf_size: the size of the receiving buffer used in recv() calls, in bytes."""
        self.port_number = port_number
        self.rec_buf_size = rec_buf_size

        self._id = "" if self.port_number is None else str(self.port_number)

        #local read buffer, currently with no size limit
        self._read_buffer= bytearray(b'')
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

    def read_message(self, connection):
        """ Reads a single message from the recv buffer, as specified by the format in protocol.py:
            expects the first 9 bytes to give the length of the remainer of the messsage."""
        prefix = self._read(connection, PREFIX_SIZE)
        msg_len = decode_length(prefix)
        msg = self._read(connection, msg_len)
        self.log(f"{self._id} RECD: {msg}")
        return msg

    def send_message(self, socket, message_body):
        """ Sends a message over the given socket.
            message_body: a bytes object"""
        socket.sendall(encode(message_body))
        

class Server(TCPModule):

    def __init__(self, port_number, rec_buf_size=1024, queue_size=1):
        """port_number: int. port number to bind to.
            rec_buf_size: size of the receive buffer in bytes
            queue_size: how many connections to allow to queue up
        """
        super().__init__(port_number=port_number, rec_buf_size=rec_buf_size)
        self._queue_size = queue_size
        self._id = F"SVR {port_number}"

    def _get_response(self):
        return b'I got this message: ' + self._chunk

    def _respond(self, connection):
        """Issue a response over the given connection. Depends on server state."""
        self.send_message(connection, self._get_response())

    def start(self):
        """Starts running the server: OPEN the local port, with no foreign socket specified.
        """
        self.log(f"Starting server listening at port {self.port_number}...")
        # create an IP socket
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
            # set the port number
            s.bind(('localhost', self.port_number))
            #allows the socket to accept connections
            s.listen(self._queue_size)
            try:
                while True:
                    # blocks until a connection is received
                    connection, address = s.accept()
                    self.log(f"Accepted a connection from {address}")
                    with connection:
                        self.read_message(connection)
                        self._respond(connection)
                        
            except KeyboardInterrupt:
                self.log("Closing server, goodbye!")    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=50000, type=int)
    args = parser.parse_args()
    server = Server(args.port, rec_buf_size=1024, queue_size=1)
    logging.basicConfig(level=logging.INFO)
    server.start()
