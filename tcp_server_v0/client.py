import argparse
import socket
import sys

from server import TCPModule

class Client(TCPModule):

    def __init__(self, port_number=None, rec_buf_size=1024):
        super().__init__(port_number=port_number, rec_buf_size=rec_buf_size)
        if self.port_number is not None:
            self.port_number = int(self.port_number)

    def set_port_number(self, n):
        """Updates the current port number of this client."""
        self.port_number = n
        self._id = f"CLT {self.port_number}"

    def send(self, foreign_addr, foreign_port, message):
        """Send a bytes message to TCP server at address and port specified."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.log(f"Connecting to {foreign_addr}, port {foreign_port}...")

            if self.port_number is not None:
                self.log(f"Binding to local port {self.port_number}...")
                s.bind(('127.0.0.1', self.port_number))
            s.connect((foreign_addr, foreign_port))

            self.set_port_number(s.getsockname()[1])
            self.log(f"Using local port {self.port_number}")

            self.send_message(s, message)
            self.log(f"Message sent.")
            self.read_message(s)
        self.log("Done.")
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("msg", default="", type=str)
    parser.add_argument("-target", default=50000, type=int)
    parser.add_argument("--port", default=None)
    args = parser.parse_args()

    message = bytes(args.msg, 'ascii')
    cl = Client(port_number=args.port)
    cl.send('127.0.0.1', args.target, message)
