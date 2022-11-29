from agent.shared_memory_agent import SharedMemoryAgent


shared_memory_agnet = SharedMemoryAgent()

shared_memory_agnet.create_server()

input_str = ""
while input_str.upper() != "Q":

    input_str = input("Shared Memory Clinet is Running...\n")

shared_memory_agnet.close_server()

print("bye!")
