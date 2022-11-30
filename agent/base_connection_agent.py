from abc import ABC, abstractmethod
import logging
from multiprocessing import Process
from multiprocessing.connection import Listener, Connection, Client
from threading import Thread
import time

from agent.base_agent import BaseAgent, main_process, ServerModel
from datetime import datetime, timedelta


logger = logging.getLogger(__name__)


class ConnectionProcess(Thread):
    def __init__(self, conn):
        super().__init__()
        self._conn = conn

    def run(self):
        self.connection_process()

    def connection_process(self):
        out_of_time = datetime.now() + timedelta(seconds=600)
        try:
            while out_of_time > datetime.now():
                received_bytes = self._conn.recv_bytes()
                if len(received_bytes) == 0:
                    break
                else:
                    received_str = received_bytes.decode()
                    response_str = main_process(received_str)
                    self._conn.send_bytes(response_str.encode())

        except Exception as exc:
            print(exc)

        return ""


class ConnectionServer(Thread):
    def __init__(self, server_model: ServerModel, listener, address, family):
        super().__init__()
        self.address = address
        self.listener = listener
        self.family = family
        self.server_model = server_model

    def run(self):
        print(f"Server is running ({self.address})  ")
        while self.server_model.status.upper() != "Q":
            _conn = self.listener.accept()
            # connection_process(_conn)
            connection_process = ConnectionProcess(_conn)
            connection_process.daemon = True
            connection_process.start()


class BaseConnectionAgent(BaseAgent):
    def __init__(self, *args) -> None:
        super().__init__(*args)
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
        conn_server = ConnectionServer(
            self._server_model, listener, self.get_address(), self.get_family()
        )
        conn_server.daemon = True
        conn_server.start()

    def close_server(self):
        self._server_model.status = "Q"

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
                        return

            except Exception as exc:
                logger.warning(exc)
                print(f"Waitting For Retry ({i+1})")
                time.sleep(wait_sec)
        raise Exception("Connection Error.")

    def close(self):
        self._conn.close()
