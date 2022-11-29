from agent.socket_agent import SocketAgent


socket_agent = SocketAgent()

socket_agent.create_server()


input_str = ""
while input_str.upper() != "Q":
    input_str = input("Socket Client is Running...\n")

socket_agent.close_server()

print("bye!")
