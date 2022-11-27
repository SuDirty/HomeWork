

from datetime import datetime, timedelta
import logging
import os
import time


logger = logging.getLogger(__name__)


class PipeFile():
    def __init__(self, name, trunc_flag=False):
        self.name = name
        self.fd = None
        self.trunc_flag = trunc_flag

    def __enter__(self):
        if self.trunc_flag:
            self.fd = os.open(self.name, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        else:
            self.fd = os.open(self.name, os.O_CREAT | os.O_RDWR)

        return self

    def __exit__(self, type, value, traceback):
        # Exception handling here
        os.close(self.fd)
        if self.trunc_flag:
            os.unlink(self.name)


class PipeAgent:

    def __init__(self, pipe_name: str = "test_pipe") -> None:
        self.pipe_name = pipe_name
        self.pipe_in = None
        self.pipe_out = None

        pass

    def create_pipe_server(self):
        with PipeFile(f"tmp/{self.pipe_name}_in.pipe") as self.pipe_in:
            with PipeFile(f"tmp/{self.pipe_name}_out.pipe") as self.pipe_out:
                line_bytes = b""
                while True:
                    read_bytes: bytes = os.read(self.pipe_in.fd, 1)
                    if len(read_bytes) != 0:
                        if read_bytes == b"\0":
                            read_str = line_bytes.decode()
                            logger.info(read_str)
                            if read_str == "Hello":
                                self.send("Hello")
                            line_bytes = b""
                        else:
                            line_bytes += read_bytes

    def try_connect(self, retry_times: int = 10, wait_sec: int = 10, time_out: int = 5):
        with PipeFile(f"tmp/{self.pipe_name}_out.pipe", False) as self.pipe_in:
            with PipeFile(f"tmp/{self.pipe_name}_in.pipe", False) as self.pipe_out:

                for i in range(retry_times):
                    try:
                        self.send("Hello")
                        line_bytes = b""
                        out_of_time = datetime.now() + timedelta(seconds=time_out)
                        while True:
                            if datetime.now() > out_of_time:
                                raise Exception("Connection Timeout")
                            read_bytes: bytes = os.read(self.pipe_in.fd, 1)
                            if len(read_bytes) != 0:
                                if read_bytes == b"\0":
                                    read_str = line_bytes.decode()
                                    logger.info(read_str)
                                    print(read_str)
                                    if read_str == "Hello":
                                        return True
                                    line_bytes = b""
                                else:
                                    line_bytes += read_bytes
                    except Exception as exc:
                        logger.warning(exc)
                        print(f"Waitting For Retry ({i+1})")
                        time.sleep(wait_sec)
        raise Exception("Connection Error.")

    def send(self, send_str: str = ""):
        send_bytes = f"{send_str}\0".encode()
        os.write(self.pipe_out.fd, send_bytes)
