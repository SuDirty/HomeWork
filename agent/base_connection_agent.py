from abc import ABC, abstractmethod
import logging
from multiprocessing import Process
from multiprocessing.connection import Listener, Connection, Client
import time

from agent.base_agent import BaseAgent, main_process
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


def connection_process(_conn: Connection):
    out_of_time = datetime.now() + timedelta(seconds=600)
    try:
        while out_of_time > datetime.now():
            received_bytes = _conn.recv_bytes()
            if len(received_bytes) == 0:
                break
            else:
                received_str = received_bytes.decode()
                response_str = main_process(received_str)
                _conn.send_bytes(response_str.encode())

    except Exception as exc:
        print(exc)

    return ""


class BaseConnectionAgent(BaseAgent):
    def __init__(self, *args) -> None:
        self._conn: Connection = None

    @abstractmethod
    def get_family(self):
        pass

    @abstractmethod
    def get_address(self):
        pass

    def request_message(self, send_msg: str, time_out: int = 60):
        if self._conn is None or self._conn.closed:
            self.try_connect()

        self._conn.send_bytes(send_msg.encode())
        out_of_time = datetime.now() + timedelta(seconds=time_out)
        while out_of_time > datetime.now():
            received_bytes = self._conn.recv_bytes()
            if received_bytes:
                return received_bytes.decode()

        raise Exception("Connection Timeout.")

    def create_server(self):
        listener = Listener(address=self.get_address(), family=self.get_family())
        while True:
            self._conn = listener.accept()
            p = Process(target=connection_process, args=(self._conn,))
            p.start()
            p.join()

    def try_connect(self, try_times: int = 10, wait_sec: int = 10):
        for i in range(try_times):
            try:
                self._conn = Client(self.get_address())
                self._conn.send_bytes(b"Handshake")
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

    def close(self):
        self._conn.close()
