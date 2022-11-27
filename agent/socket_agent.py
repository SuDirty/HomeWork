from datetime import datetime
import logging
import socket
import sys
import time
from agent.base_connection_agent import BaseConnectionAgent


logger = logging.getLogger(__name__)


class SocketAgent(BaseConnectionAgent):

    def __init__(self, *args, host: str = None, port: int = 9999) -> None:
        super().__init__()
        self.host = host if host else socket.gethostname()
        self.port = port

    def get_address(self):
        return (self.host, self.port)

    def get_family(self):
        return "AF_INET"
