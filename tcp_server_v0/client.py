import socket

class Client:

    def __init__(self, port_number=None, rec_buf_size=1024):
        self.port_number = port_number
        self.rec_buf_size = rec_buf_size

    def log(self, s):
        print(s)

    def send(self, foreign_addr, foreign_port, message):
        """Send a bytes message to TCP server at address and port specified."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            self.log(f"Connecting to {foreign_addr}, port {foreign_port}...")
            if self.port_number is not None:
                s.bind(('', self.port_number))
            s.connect((foreign_addr, foreign_port))
            self.log(f"Using local socket {s.getsockname()}")
            nb = s.send(message)
            self.log(f"{nb} bytes sent.")
        self.log("Done.")
        

if __name__ == "__main__":
    cl = Client(port_number=61877)
    cl.send('127.0.0.1', 56500, b'hello')