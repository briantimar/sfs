""" A toy server using python's sockets module - just to demonstrate how to use the TCP api"""
import logging
import socket

class Server:

    def __init__(self, port_number, rec_buf_size=1024, queue_size=1):
        """port_number: int. port number to bind to.
            rec_buf_size: size of the receive buffer in bytes
        """
        self.port_number = port_number
        self.rec_buf_size = rec_buf_size
        self._queue_size = queue_size
        
        #read bytes objects into here
        self._read_buffer = []
        #full bytes object that was last read
        self._read = b''

    def log(self, s):
        # logging.info(s)
        print(s)

    def flush_read(self):
        """Flush the read buffer."""
        self._read = b''.join(self._read_buffer)
        self._read_buffer = []

    def start(self):
        """Starts running the server: OPEN the local port, with no foreign socket specified.
        """
        self.log(f"Starting server listening at port {self.port_number}...")
        # create an IP socket
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
                        # now, receive data from the connection, and close when the buffer empties.
                        data = connection.recv(self.rec_buf_size)
                        while data:
                            self._read_buffer.append(data)
                            data = connection.recv(self.rec_buf_size)
                        self.flush_read()
                        print(f"Received data: {self._read}")
            except KeyboardInterrupt:
                self.log("Closing server, goodbye!")    


if __name__ == "__main__":
    server = Server(56500, rec_buf_size=2)
    logging.basicConfig(level=logging.INFO)
    server.start()
