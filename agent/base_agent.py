from abc import ABC, abstractmethod
import logging
import sys
from time import sleep

from services.math_service import get_mean, get_median, get_mode

logger = logging.getLogger(__name__)


class ServerModel:
    def __init__(self):
        self.status = ""


def main_process(received_str):
    try:
        if received_str == "Handshake":
            return "Handshake"

        if ":" in received_str:
            temp_str_list = received_str.split(":")

            process_name = temp_str_list[0]
            process_parameter = temp_str_list[1]
            str_list = process_parameter.split(" ")

            float_list = [float(tmp_str) for tmp_str in str_list if tmp_str != ""]

            result = {"Mean": get_mean, "Median": get_median, "Mode": get_mode}.get(process_name)(
                float_list
            )

            response_str = {
                "Mean": "MeanResult:",
                "Median": "MedianResult:",
                "Mode": "ModeResult:",
            }.get(process_name) + str(result)
            return response_str

    except Exception as exc:
        return "Error:" + str(exc).encode()
    return ""


class BaseAgent(ABC):
    def __init__(self, *args) -> None:
        self._server_model = ServerModel()

    @abstractmethod
    def get_family(self):
        pass

    @abstractmethod
    def get_address(self):
        pass

    @abstractmethod
    def request_message(self, send_msg: str, time_out: int = 60):
        pass

    @abstractmethod
    def create_server(self):
        pass

    @abstractmethod
    def try_connect(self, try_times: int = 10, wait_sec: int = 10):
        pass

    @abstractmethod
    def close(self):
        pass


    def keep_server(self):
        keep_time = 600
        if len(sys.argv) > 0 :
            try:
                keep_time = int(sys.argv[1])
            except Exception as exc:
                pass
        print(f'The server will be on for {keep_time} seconds')
        sleep(keep_time)