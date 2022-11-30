from datetime import datetime, timedelta
import logging
from multiprocessing.resource_tracker import unregister
from multiprocessing.shared_memory import SharedMemory
import os
from threading import Thread
import time

from agent.base_agent import BaseAgent, main_process, ServerModel

logger = logging.getLogger(__name__)


class SharedMemoryServer(Thread):
    def __init__(self, server_model: ServerModel, address):
        super().__init__()
        self.address = address
        self.server_model = server_model
        self._sm_in = None
        self._sm_out = None

    def run(self):
        try:
            while self.server_model.status.upper() != "Q":
                self._get_shared_memory()
                for idx, buf_byte in enumerate(self._sm_in.buf):
                    if 0 == buf_byte:
                        temp_bytes = bytes(self._sm_in.buf[:idx])
                        if len(temp_bytes) != 0:

                            result_str = main_process(temp_bytes.decode())
                            if result_str:
                                self.send(self._sm_out, result_str)
                                self.send(self._sm_in, "\0")
                        break

                time.sleep(1)
        except Exception as exc:
            print(exc)
            
    def send(self, sm_out: SharedMemory, send_str: str):
        send_str += "\0"
        sm_out.buf[: len(send_str)] = bytes(send_str.encode())

    def _get_shared_memory(self):
        try:
            self._sm_out: SharedMemory = SharedMemory(name=f"psm_{self.address}_out", size=1024)
            self._sm_in: SharedMemory = SharedMemory(name=f"psm_{self.address}_in", size=1024)
        except FileNotFoundError as exc:
            print("Create new shared memory")
            self._sm_out: SharedMemory = SharedMemory(
                name=f"psm_{self.address}_out", create=True, size=1024
            )
            self._sm_in: SharedMemory = SharedMemory(
                name=f"psm_{self.address}_in", create=True, size=1024
            )
            return 


class SharedMemoryAgent(BaseAgent):
    def __init__(self, *args, name="named_memory") -> None:
        super().__init__(*args)
        self._conn_name: str = name
        self._sm_out = None
        self._sm_in = None

    def get_family(self):
        pass

    def get_address(self):
        return self._conn_name

    def request_message(self, send_msg: str, time_out: int = 60):
        self.send(self._sm_out, send_msg)
        out_of_time = datetime.now() + timedelta(seconds=600)
        while out_of_time > datetime.now():
            for idx, buf_byte in enumerate(self._sm_in.buf):
                if 0 == buf_byte:
                    temp_bytes = bytes(self._sm_in.buf[:idx])
                    if len(temp_bytes) != 0:
                        self.send(self._sm_in, "")
                        return temp_bytes.decode()
                    break

    def create_server(self):
        self._sm_out = None
        self._sm_in = None

        server = SharedMemoryServer(self._server_model, self.get_address())
        server.daemon = True
        server.start()

    def close_server(self):
        self._server_model.status = "Q"

    def try_connect(self, try_times: int = 10, wait_sec: int = 10):
        for i in range(try_times):
            try:
                self._sm_out: SharedMemory = SharedMemory(f"psm_{self.get_address()}_in")
                self._sm_in: SharedMemory = SharedMemory(f"psm_{self.get_address()}_out")

                self.send(self._sm_out, "Handshake")
                while True:
                    temp_bytes = ""
                    for idx, buf_byte in enumerate(self._sm_in.buf):
                        if 0 == buf_byte:
                            temp_bytes = bytes(self._sm_in.buf[:idx])
                            if temp_bytes == b"Handshake":
                                self.send(self._sm_in, "")
                                return

                            break

            except Exception as exc:
                logger.warning(exc)
                print(f"Waitting For Retry ({i+1})")
                time.sleep(wait_sec)
        raise Exception("Connection Error.")

    def send(self, sm_out: SharedMemory, send_str: str):
        send_str += "\0"
        sm_out.buf[: len(send_str)] = bytes(send_str.encode())

    def close(self):
        self._sm_in.close()
        self._sm_out.close()
        pass
