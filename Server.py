# TCP chat server
################
# Do not print anything other than chat msg
################

import socket
import select
import argparse
import sys


# Broadcast chat message to all the client user in the chat room
def broadcast_data (s, message):

    # don't send msg to server and msg owner
    for socket in connections:
        if socket != server_socket:
            #and socket != s :
            try :
                print("try to broadcast ", message)
                socket.send(message.encode())
            except :
                # exit chat room
                socket.close()
                connections.remove(socket)

# show text in line
def client_prompt() :
    sys.stdout.write('<You> ')
    sys.stdout.flush()



def server_mode():
    print("Server socket is start on port: ", PORT)
    msg = ""

    while msg != "exit":
        # Get read,writes error's sockets list
        read_sockets,write_sockets,error_sockets = select.select(connections,[],[])

        for s in read_sockets:

            # When a client connect to server
            if s == server_socket:
                s_client, addr = server_socket.accept()
                connections.append(s_client)
                print(addr)
                print("Client ", addr, "connected.")
                msg = "Client "+ str(addr) + " entered the chat room."
                # broadcast enter msg to all user in chat room
                broadcast_data(s_client,msg)

            else:

                try:
                    data = s.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(s, "r" + ' ' + data)
                except:
                    msg = "Client "+ str(addr) + " is offline."
                    broadcast_data(s, msg)
                    s.close()
                    connections.remove(s)
                    continue

    server_socket.close()

def client_mode(hostname):
    print(hostname)
    host = socket.gethostname()#hostname
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(2)

    # connect to remote host
    #s.connect((host,port))

    try:
        s.connect((host,port))
    except:
        print ("Unable to connect")
        sys.exit()


    client_prompt()

    while True:
        socket_list = [sys.stdin, s]

        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for client_socket in read_sockets:
            #incoming message from remote server
            if client_socket == s:
                data = client_socket.recv(1024).decode()
                print("data ",data)
                sys.stdout.write(data)
                client_prompt()

                '''
                if not data :
                    print("Disconnected from chat server")
                    sys.exit()
                
                else :
                    #print data
                    sys.stdout.write(data)
                    client_prompt()
                '''



            #user entered a message
            else :
                msg = input()
                s.send(msg.encode())
                client_prompt()



if __name__ == "__main__":
    # List to keep track of server socket
    connections = []

    # use para to select mode of this program
    # use -s start server mode
    # use -c start client mode
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', default=False, dest='select_Mode',
                       help='Indicates the program should wait for an incoming TCP/IP connection on port 9999')

    parser.add_argument('-c', action='store', dest='hostname',
                    help='Store hostname')
    results = parser.parse_args()

    # run a server
    if results.select_Mode:
        RECV_BUFFER = 1024
        PORT = 9999 # Set server's port as 9999
        host = socket.gethostname()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, PORT))
        server_socket.listen(10)  # max client num
        connections.append(server_socket)

        server_mode()

    # run a client
    elif results.hostname != None:
        hostname = results.hostname
        client_mode(hostname)




