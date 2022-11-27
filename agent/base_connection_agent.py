from abc import ABC, abstractmethod
import logging
from multiprocessing.connection import Listener, Connection, Client
import time


logger = logging.getLogger(__name__)


class BaseConnectionAgent(ABC):

    def __init__(self, *args) -> None:
        self._conn: Connection = None

    @abstractmethod
    def get_family(self):
        pass

    @abstractmethod
    def get_address(self):
        pass

    def create_server(self):
        listener = Listener(
            address=self.get_address(), family=self.get_family())
        while True:
            self._conn = listener.accept()
            while True:
                received_bytes = self._conn.recv_bytes()
                if len(received_bytes) == 0:
                    break
                else:
                    received_str = received_bytes.decode()
                    if received_str == "Hello":
                        self._conn.send_bytes(b"Hello")

    def try_connect(self, try_times: int = 10, wait_sec: int = 10):
        for i in range(try_times):
            try:
                self._conn = Client(self.get_address())
                self._conn.send_bytes(b"Hello")
                logger.debug(f"Connected {self.get_address()}")
                while True:
                    received_bytes = self._conn.recv_bytes()
                    if received_bytes:
                        logger.debug(received_bytes)
                        print(received_bytes.decode())
                        return

            except Exception as exc:
                logger.warning(exc)
                print(f"Waitting For Retry ({i+1})")
                time.sleep(wait_sec)
        raise Exception("Connection Error.")
