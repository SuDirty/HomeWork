from datetime import datetime
import logging
import socket
import sys
import time



logger = logging.getLogger(__name__)

class SocketAgent:

    def __init__(self, host: str = None, port: int = 9999) -> None:
        self.host = host if host else socket.gethostname()
        self.port = port
        self.client_socket = None

    def create_socket_server(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        while True:
            clientsocket, addr = server_socket.accept()            
            logger.debug("client connected")

            self.client_socket = clientsocket

            connection_start_time = datetime.now()
            while True:
                received_bytes = self.client_socket.recv(1024)
                if len(received_bytes) != 0:
                    logger.debug(received_bytes)
                    self.client_socket.send(f"{received_bytes} too.".encode())

    def try_connect(self, try_times:int = 10, wait_sec:int = 10):
        for i in range(try_times):
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host,self.port))
                self.client_socket = client_socket

                self.client_socket.send("Hello".encode())
                logger.debug(f"Connected {self.host}:{self.port}")
                while True:
                    received_bytes = self.client_socket.recv(1024)
                    if received_bytes:
                        logger.debug(received_bytes)
                        return

            except Exception as exc:
                logger.warning(exc)
                print(f"Waitting For Retry ({i+1})")
                time.sleep(wait_sec)
        raise Exception("Connection Error.")