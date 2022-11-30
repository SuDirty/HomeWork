import sys
from time import sleep
from agent.shared_memory_agent import SharedMemoryAgent


shared_memory_agnet = SharedMemoryAgent()

shared_memory_agnet.create_server()

shared_memory_agnet.keep_server()

shared_memory_agnet.close_server()

print("bye!")
