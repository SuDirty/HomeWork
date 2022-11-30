import sys
from time import sleep
from agent.pipe_agent import PipeAgent


pipe_agnet = PipeAgent()

pipe_agnet.create_server()

pipe_agnet.keep_server()

pipe_agnet.close_server()

print("bye!")
