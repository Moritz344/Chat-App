#-----------------------------------------------------------------------------#
# Listening for upcoming client connections ,
# if a new client is connected, we add it to our collection of client sockets.

# Start a new thread for each connected client that keeps listening to upcoming
# messages sent from the client and broadcasts them to all other clients.
#----------------------------------------------------------------------------#

import socket
from threading import Thread
# server IP

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 

seperator_token = "<SEP>" # sepearetes client name & messages

# Init list/set of all connected clients sockets
client_sockets = set()

# TCP socket
s = socket.socket()

# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

# bind the socket to teh address we specified
s.bind((SERVER_HOST,SERVER_PORT))

# listens for upcoming connections
s.listen(5)


print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")


def listen_for_client(cs):
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """

    while True:
        try:
            # keep listening for a message from 'cs' socket
            msg = cs.recv(1024).decode()

        except Exception as e:
            # client no longer connected
            
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)

        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing

            msg = msg.replace(seperator_token, ":")

        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message

            client_socket.send(msg.encode())


while True:
    # we keep listening for new connections all the time
    client_socket,client_address = s.accept()
    print(f"[+] {client_address} connected .")

    # add the new connected client to connected sockets
    client_sockets.add(client_socket)

    # start a new thread that listens for each clients messages
    t = Thread(target=listen_for_client,args=(client_socket,))

    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True

    # start the thread
    t.start()

# close client sockets
for cs in client_sockets:
    cs.close()

# close server socket
s.close()











