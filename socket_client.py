import sys
from time import sleep
from agent.socket_agent import SocketAgent


socket_agent = SocketAgent()

socket_agent.create_server()

socket_agent.keep_server()

socket_agent.close_server()

print("bye!")
