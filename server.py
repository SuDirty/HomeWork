import logging
from agent.pipe_agent import PipeAgent
from agent.socket_agent import SocketAgent
from agent.shared_memory_agent import SharedMemoryAgent
import re


logger = logging.getLogger(__name__)


# 嘗試連線 Client 1 via socket
socket_agent = SocketAgent()
socket_agent.try_connect()
print("Client 1 is ready.")

# 嘗試連線 Client 2 via pipe

pipe_agent = PipeAgent()
pipe_agent.try_connect()
print("Client 2 is ready.")

# # 嘗試連線 Client 3 via shared memory

shared_memory_agent = SharedMemoryAgent()
shared_memory_agent.try_connect()
print("Client 3 is ready.")

# Wait for user input
while True:
    input_str = input(
        "Server is ready. You can type intergers and then click [ENTER].  Clients will show the mean, median, and mode of the input values."
    )

    # Verify input data
    re_compile = re.compile(r"^(\d*\s*)*$")
    match_results = re_compile.match(input_str)
    if match_results:
        break
    else:
        print("Can only be numbers.")


# Send to Client 1
response_msg = socket_agent.request_message(f"Mean:{input_str}")
print(response_msg)

# Send to Client 2
response_msg = pipe_agent.request_message(f"Median:{input_str}")
print(response_msg)

# Send to Client 3
response_msg = shared_memory_agent.request_message(f"Mode:{input_str}")
print(response_msg)


socket_agent.close()
pipe_agent.close()
shared_memory_agent.close()
