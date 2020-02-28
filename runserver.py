import argparse
import logging
from http_server.server import Server

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()
    server = Server(args.port, rec_buf_size=1024, queue_size=10, timeout=1)
    logging.basicConfig(level=logging.INFO)
    server.start()
