from datetime import datetime
import socket

HEADER = 255
PORT = 10242
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
WHO_MESSAGE = "Hi, I'm Nataliia Hrytsyshyn\nAnd it's an amazing app for finding a number by dichotomy and the golden sectionmethod"
ADDRESS = (SERVER, PORT)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
now = datetime.now()
CONNECT_TIME = now.strftime("%d/%m/%Y %H:%M:%S")

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' '*(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    ddd = (client.recv(2048).decode(FORMAT))
    print(ddd)
    if ddd == "Magic element is less" or ddd == "Magic element is greater" or ddd == WHO_MESSAGE:
        return "green"
    return "red"

flag = "green"
game = "Find number between 0 and 1000000\U0001f600"
print(game.center(75))
messages = []
while flag == "green":
    try:
        user_input = input("What's the number? ")
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")
        messages.append(f"Client message at {time}: {user_input}\n")
        if user_input == DISCONNECT_MESSAGE:
            send(user_input)
            break
        if user_input != "Who":
            user_input = int(user_input)
        flag = send(str(user_input))
    except ValueError:
        pass

my_file = open("sys_magazine.txt", "a")
my_file.write("\n")
my_file.write(f"Connected to server at {CONNECT_TIME}\n")  
for i in range(len(messages)):
    my_file.write(messages[i])
my_file.write(f"Number found successfully at {time}")
my_file.close()