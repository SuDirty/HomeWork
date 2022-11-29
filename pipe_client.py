from agent.pipe_agent import PipeAgent


pipe_agnet = PipeAgent()

pipe_agnet.create_server()


input_str = ""
while input_str.upper() != "Q":

    input_str = input("Pipe Clinet is Running...\n")

pipe_agnet.close_server()

print("bye!")
