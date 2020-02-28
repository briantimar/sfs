""" A toy server using python's sockets module - just to demonstrate how to use the TCP api"""
import logging
import socket
import argparse
import threading

from .tcp import TCPModule

def handle_connection(connection, rec_buf_size):
    """Handles a single TCP connection (represented by a connected socket)"""
    with connection:
        print(f"Thread opened for connection at {connection.getsockname()} to {connection.getpeername()}")
        chunk = connection.recv(rec_buf_size)
        print(chunk)
    print("thread finished.")
    return

class Server(TCPModule):
    """Accepts connections and dispatches them to individual endpoints."""

    def __init__(self, port_number, rec_buf_size=1024, queue_size=10, timeout=None):
        """port_number: int. port number to bind to.
            rec_buf_size: size of the receive buffer in bytes
            queue_size: how many connections to allow to queue up
        """
        super().__init__(port_number=port_number, rec_buf_size=rec_buf_size, timeout=timeout)
        self._queue_size = queue_size
        self._id = F"SVR {port_number}"
        self.threads = []

    def make_thread(self, connection):
        th = threading.Thread(target=handle_connection, args=(connection,self.rec_buf_size))
        self.threads.append(th)
        return th

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
                    cl_thread = self.make_thread(connection)
                    cl_thread.start()

            except KeyboardInterrupt:
                self.log("Closing server, goodbye!")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()
    server = Server(args.port, rec_buf_size=1024, queue_size=10)
    logging.basicConfig(level=logging.INFO)
    server.start()
