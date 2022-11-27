import logging
from multiprocessing.shared_memory import SharedMemory
from multiprocessing.managers import SharedMemoryManager
import time

from agent.base_connection_agent import BaseConnectionAgent


logger = logging.getLogger(__name__)


class SharedMemoryAgent(BaseConnectionAgent):
    def __init__(self, *args, name='test_memory_name') -> None:
        self._conn_name: str = name
        self._sm_out = None
        self._sm_in = None

    def get_family(self):
        pass

    def get_address(self):
        return self._conn_name

    def create_server(self):
        self._sm_out = None
        self._sm_in = None
        try:
            self._sm_out: SharedMemory = SharedMemory(
                name=f"psm_{self.get_address()}_out",
                create=True, size=1024)
            self._sm_in: SharedMemory = SharedMemory(
                name=f"psm_{self.get_address()}_in",
                create=True, size=1024)
            while True:
                for idx, buf_byte in enumerate(self._sm_in.buf):
                    if 0 == buf_byte:
                        temp_bytes = bytes(self._sm_in.buf[:idx])
                        if temp_bytes == b'Hello':
                            print(temp_bytes)
                            self.send(self._sm_out, "Hello")
                            self.send(self._sm_in, "\0")
                        if temp_bytes == b"Exit":
                            return
                        break
        except Exception as exc:
            logger.error(exc)
            print(exc)
        finally:

            if self._sm_in:
                self._sm_in.close()
                self._sm_in.unlink()
            if self._sm_out:
                self._sm_out.close()
                self._sm_out.unlink()

            if not self._sm_out:
                self._sm_out = SharedMemory(
                    name=f"psm_{self.get_address()}_out", size=1024)

                self._sm_out.close()
                self._sm_out.unlink()
            if not self._sm_in:
                self._sm_in = SharedMemory(
                    name=f"psm_{self.get_address()}_in", size=1024)

                self._sm_in.close()
                self._sm_in.unlink()

    def try_connect(self, try_times: int = 10, wait_sec: int = 10):
        for i in range(try_times):
            try:
                self._sm_out: SharedMemory = SharedMemory(
                    f"psm_{self.get_address()}_in")
                self._sm_in: SharedMemory = SharedMemory(
                    f"psm_{self.get_address()}_out")

                self.send(self._sm_out, "Hello")
                while True:
                    temp_bytes = ""
                    for x in range(len(self._sm_in.buf)):
                        if 0 == self._sm_in.buf[x]:
                            temp_bytes = bytes(self._sm_in.buf[:x])
                            if temp_bytes == b'Hello':
                                print(temp_bytes)
                                self.send(self._sm_in,"\0")
                                return
                            else:
                                break

            except Exception as exc:
                logger.warning(exc)
                print(exc)
                print(f"Waitting For Retry ({i+1})")
                time.sleep(wait_sec)
            finally:
                if self._sm_in:
                    self._sm_in.close()
                if self._sm_out:
                    self._sm_out.close()
        raise Exception("Connection Error.")

    def send(self, sm_out: SharedMemory, send_str: str):
        sm_out.buf[:len(send_str)] = bytes(send_str.encode())
