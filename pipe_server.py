import multiprocessing
import os
import time





# 初始化 Server

# 嘗試連線 Client 1 via socket

# 嘗試連線 Client 2 via pipe

# 嘗試連線 Client 3 via shared memory

# Wait for user input

# Verify input data

# Send to Client 1

# Send to Client 2

# Send to Client 3








process = multiprocessing.current_process()
process_list = []

def cut_bytes(input_bytes:bytes , cut_len):
    return [input_bytes[i:i+cut_len] for i in range(0,len(input_bytes),cut_len)]

while len(process_list) == 0:
    process_list = [ file_name for file_name in os.listdir('tmp/') if "server_out" in file_name]
    time.sleep(1)
    if not process_list:
        print("Waiting For pipe client.....")

write_path = process_list[0]
print(f"found pipe tmp/{write_path}")

wf = None
if wf == None:
    wf = os.open(f"tmp/{write_path}",os.P_WAIT | os.O_RDWR)

close_flag = False
count_str = 1
while not close_flag :
    # user_input = input('Please input int array or "Q" to exit:')
    count_str += 1
    user_input = str(count_str)
    if user_input.upper() == "Q" or count_str == 10000:
        close_flag = True
        print('Bye~')

    else:
        user_input = f"{process.pid}:{user_input}\0"
        for send_str in cut_bytes(user_input,10):
            os.write(wf,send_str.encode('utf-8'))

