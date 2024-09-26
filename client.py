"""
    Connects to the server.
    Keep listening for messages coming from the server
    (must be a client sent a message to the server and the server broadcasted it)
    and print it to the console.
    Waiting for the user to input messages to send to the server.
"""

import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore,init,Back



# init colors
init()

name = input("Enter your name: ")

# set available colors

colors = [Fore.RED,Fore.BLUE,Fore.CYAN,Fore.GREEN,Fore.LIGHTBLACK_EX,
          Fore.LIGHTBLUE_EX,Fore.LIGHTCYAN_EX
]

client_color = random.choice(colors)
leave_color = colors[0]
join_color = Fore.GREEN
# server IP ADRESS


SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server port
seperator_token = "<SEP>" 



# init TCP SOCKET
s = socket.socket()

print(f"[*] Connection to {SERVER_HOST}:{SERVER_PORT}...")

# connect to the server
s.connect((SERVER_HOST,SERVER_PORT))
print("[+] Connected.")
def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        print("\n" + message)


# make a thread that listens for messages to this client & print them

t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True

# start the thread
t.start()


join_message = f"{join_color}{name} joined the chat :)." 
s.send(join_message.encode())

while True:

   # input message we want to send to the server
    to_send = input("You: ")
    leaving_message = None
    # a way to exit the program
    if to_send == "q":
        print("You left the chat room.")
        leaving_message = f"{leave_color}{name} left the chat room :( {Fore.RESET}"
        s.send(leaving_message.encode())
        break
    


    # add the datetime, name & the color of the sender
    
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    to_send = f"{client_color}[{date_now}] {name}{seperator_token}{to_send}{Fore.RESET}"

    # finally, send the message
    s.send(to_send.encode())


# close the socket
s.close()

