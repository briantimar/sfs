""" A toy server using python's sockets module - just to demonstrate how to use the TCP api"""
import logging
import socket

class TCPModule:
    """One half of a TCP connection."""

    def __init__(self, port_number=None, rec_buf_size=1024):
        """port_number: if provided, will attempt to bind to this port number.
        rec_buf_size: the size of the receiving buffer used in recv() calls, in bytes."""
        self.port_number = port_number
        self.rec_buf_size = rec_buf_size

        #read individual recv calls into here
        self._read_buffer = []
        # the result of a 'full read' operation
        self._read = b''

    def log(self, s):
        print(s)

    def flush_read(self):
        """Flush the read buffer."""
        self._read = b''.join(self._read_buffer)
        self._read_buffer = []

    def _read_all(self, connection):
        """Read bytes from the given connection into the read buffer, until no more remain."""
        data = connection.recv(self.rec_buf_size)
        while data:
            self._read_buffer.append(data)
            data = connection.recv(self.rec_buf_size)
        self.flush_read()
        self.log(f"Received data: {self._read}")

class Server(TCPModule):

    def __init__(self, port_number, rec_buf_size=1024, queue_size=1):
        """port_number: int. port number to bind to.
            rec_buf_size: size of the receive buffer in bytes
            queue_size: how many connections to allow to queue up
        """
        super().__init__(port_number=port_number, rec_buf_size=rec_buf_size)
        self._queue_size = queue_size

    def _get_response(self):
        return b'I got this message: ' + self._read

    def _respond(self, connection):
        """Issue a response over the given connection. Depends on server state."""
        connection.sendall(self._get_response())

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
                        self._read_all(connection)
                        self._respond(connection)
                        
            except KeyboardInterrupt:
                self.log("Closing server, goodbye!")    


if __name__ == "__main__":
    server = Server(56500, rec_buf_size=2, queue_size=1)
    logging.basicConfig(level=logging.INFO)
    server.start()
