import os
from os.path import exists
from datetime import datetime
import logging
from multiprocessing.connection import Listener
import socket
import sys
import time

from agent.base_connection_agent import BaseConnectionAgent

logger = logging.getLogger(__name__)


class PipeAgent(BaseConnectionAgent):

    def __init__(self, *args, name: str = "test_pipe") -> None:
        super().__init__(*args)
        self.name = name

    def create_server(self):
        self.init_pipe_file()
        return super().create_server()

    def init_pipe_file(self):
        file_exists = exists(self.get_address())
        if file_exists:
            os.unlink(self.get_address())

    def get_family(self):
        if sys.platform == 'win32':
            return 'AF_PIPE'
        if sys.platform != 'win32':
            return 'AF_UNIX'

    def get_address(self):
        if sys.platform == 'win32':
            return r'\\.\pipe\pipe_' + self.name
        if sys.platform != 'win32':
            return f"tmp/{self.name}"

