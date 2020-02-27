""" A toy server using python's sockets module - just to demonstrate how to use the TCP api"""
import logging
import socket

class Server:

    def __init__(self, port_number, rec_buf_size):
        """port_number: int. port number to bind to.
            rec_buf_size: size of the receive buffer in bytes
        """

        self.port_number = port_number
        self.rec_buf_size = rec_buf_size

    def log(self, s):
        logging.info(s)

    def start(self):
        """Starts running the server: OPEN the local port, with no foreign socket specified.
        """
        self.log(f"Starting server listening at port {self.port_number}...")
        # create an IP socket
        with socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # set the port number
            s.bind(('', self.port_number))
            #allows the socket to accept connections
            s.listen(1)
            while True:
                try:
                    # blocks until a connection is received
                    connection, address = s.accept()
                    self.log(f"Accepted a connection from {address}")
                    # now, receive data from the connection
                    data = connection.recv(self.rec_buf_size)
                    self.log(f"received data: {repr(data)}")
                except KeyboardInterrupt:
                    self.log("Closing server, goodbye!")    



if __name__ == "__main__":
    server = Server(56500, 1024)
    logging.basicConfig(level=logging.INFO)
    server.start()
