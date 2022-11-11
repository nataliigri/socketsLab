from bisect import bisect_left
from datetime import datetime
import socket
from sqlite3 import connect
import threading
import time
import random
import sys

HEADER = 255
PORT = 10242
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
WHO_MESSAGE = "Hi, I'm Nataliia Hrytsyshyn\nAnd it's an amazing app for finding a number by dichotomy and the golden sectionmethod"

class Error(Exception):
    pass
try:
    METHOD = sys.argv[1]
    if METHOD != "d" and METHOD != "g":
        raise Error
except:
    sys.exit("Please choose a method \U0001F970")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
def handle_client(connection, address,CONNECT_TIME):
    print(f"New connections: {address} is connected")
    xL = 0 
    xU = 100
    arr = []
    for i in range(101):
        arr.append(i)
    it = 0
    all_time = 0
    magicEl = random.randint(xL,xU)
    connected = True
    MESSAGES = []
    my_file = open("sys_magazine.txt", "w")
    while connected:
        msg_length = connection.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = connection.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            elif msg == "Who":
                connection.send(WHO_MESSAGE.encode(FORMAT))
            else:
                print(f"{address} {msg}")
                if METHOD == "d":
                    start_time = time.process_time()
                    result = dichotomy_method(xL,xU,msg,magicEl)
                    end_time = time.process_time()
                else:
                    start_time = time.process_time()
                    result = goldenSectionSearch(arr,msg,magicEl,len(arr))
                    end_time = time.process_time()
                all_time += (end_time - start_time) 
                print(all_time)
                MESSAGES.append(f"Iteration: {it} Execution time: {str(all_time)} seconds\n")
                connection.send(f"{result}".encode(FORMAT))
                it += 1
                if result == "You nailed it!":
                    connection.send(f" Iterations: {str(it)} Execution time: {str(all_time)} seconds".encode(FORMAT))
                    
                    connected = False
    
    connection.close()
    my_file.write(f"Server initialized at {CONNECT_TIME}\n")            
    for i in range(len(MESSAGES)):
         my_file.write(MESSAGES[i])
    my_file.write(f"Number found successfully in {it} attempts\n")
    my_file.close()

def start():
    server.listen()
    print(f"Server is listening {SERVER}")
    now = datetime.now()
    CONNECT_TIME = now.strftime("%d/%m/%Y %H:%M:%S")
    
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address,CONNECT_TIME))
        thread.start()
        print(f"Active connections {threading.active_count() - 1}")
        
def dichotomy_method(xL, xU, el,magicEl):

    if int(el) > magicEl:
        xU = el
        return "Magic element is less"
    elif int(el) < magicEl:
        xL = el
        return "Magic element is greater"
    else:
        return "You nailed it!"

def goldenSectionSearch(arr,el,magicEl,n):
    i = int(el)
    # Initialize fibonacci numbers
    fibMMm2 = 0  # (m-2)'th Fibonacci No.
    fibMMm1 = 1  # (m-1)'th Fibonacci No.
    fibM = fibMMm2 + fibMMm1  # m'th Fibonacci
 
    # fibM is going to store the smallest
    # Fibonacci Number greater than or equal to n
    while (fibM < n):
        fibMMm2 = fibMMm1
        fibMMm1 = fibM
        fibM = fibMMm2 + fibMMm1
 
    # Marks the eliminated range from front
    offset = -1
 
    # while there are elements to be inspected.
    # Note that we compare arr[fibMm2] with magicEl.
    # When fibM becomes 1, fibMm2 becomes 0
    # Check if fibMm2 is a valid location
    if fibM > 1:
 
    # If magicEl is greater than the value at
    # index fibMm2, cut the subarray array
    # from offset to i
        if (arr[i] < magicEl):
            fibM = fibMMm1
            fibMMm1 = fibMMm2
            fibMMm2 = fibM - fibMMm1
            offset = i
            return "Magic element is greater"
 
    # If magicEl is less than the value at
    # index fibMm2, cut the subarray
    # after i+1
        elif (arr[i] > magicEl):
            fibM = fibMMm2
            fibMMm1 = fibMMm1 - fibMMm2
            fibMMm2 = fibM - fibMMm1
            return "Magic element is less"
 
    # magicEl found
        else:
            return "You nailed it!"

print("Server is starting")
start()