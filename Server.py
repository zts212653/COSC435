# TCP chat server
################
# Do not print anything other than chat msg
################

import socket
import select
import argparse
import sys
import queue



# Broadcast chat message to all the client user in the chat room
def broadcast_data (s, message):

    # don't send msg to server and msg owner
    for socket in outputs:
        if socket != s:
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
    print("Server socket is start on port: ", results.port)

    while True:
        # Get read,writes error's sockets list
        read_sockets,write_sockets,error_sockets = select.select(connections,outputs,[])

        for s in read_sockets:

            # When a client connect to server that is server is readable
            if s == server_socket:
                s_client, addr = server_socket.accept()
                connections.append(s_client)
                s_client.setblocking(0)
                print(addr)
                print("Client ", addr, "connected.")
                msg = "Client "+ str(addr) + " entered the chat room."
                # broadcast enter msg to all user in chat room
                message_queues[s_client] = queue.Queue()
                broadcast_data(s_client,msg)


            else:

                data = s.recv(1024).decode()
                if data:
                     message_queues[s].put(data)
                     if s not in outputs:
                        outputs.append(s)
                        #broadcast_data(s, "r" + ' ' + data)
                # when can not rev data(client has offline)

                else:
                    msg = "Client "+ str(addr) + " is offline."
                    broadcast_data(s, msg)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()
                    connections.remove(s)
                    del message_queues[s]
                    #continue

        for s in write_sockets:
            try:
                msg = message_queues[s].get()
            except queue.Empty:
                outputs.remove(s)
            else:
                broadcast_data(s,msg)


        for s in error_sockets:
            print('handling exceptional condition for', s.getpeername()[0])
            connections.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()

            del message_queues[s]


    server_socket.close()

def client_mode(hostname):
    print(hostname)
    host = socket.gethostname()#hostname
    port = int(results.port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #s.settimeout(2)

    # connect to remote host
    s.connect((host,port))

    '''
    try:
        s.connect((host,port))
    except:
        print ("Unable to connect")
        sys.exit()
    '''


    #client_prompt()

    while True:
        msg = input(">>:")
        s.send(msg.encode())
        data = s.recv(1024)
        print(data.decode())





if __name__ == "__main__":
    # Input connect to server socket
    connections = []
    # output socket list
    outputs = []
    # Message queue
    message_queues = {}

    # use para to select mode of this program
    # use -s start server mode
    # use -c start client mode
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', action='store_true', default=False, dest='select_Mode',
                       help='Indicates the program should wait for an incoming TCP/IP connection on port 9999')

    parser.add_argument('-c', action='store', dest='hostname',
                    help='Store hostname')

    parser.add_argument('-p', action='store', dest='port',
                       help='Store TCP/IP port')
    results = parser.parse_args()

    # run a server
    if results.select_Mode:
        #RECV_BUFFER = 1024
        #PORT = 9999 # Set server's port as 9999


        host = socket.gethostname()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.setblocking(False)
        server_socket.bind((host, int(results.port)))
        server_socket.listen(10)  # max client num
        connections.append(server_socket)

        server_mode()

    # run a client
    elif results.hostname != None:
        hostname = results.hostname
        client_mode(hostname)




