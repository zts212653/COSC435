# TCP chat server
################
# Do not print anything other than chat msg
################

import socket
import select
import argparse
import sys
import threading




# Broadcast chat message to all the client user in the chat room
def broadcast_data (s, message):
    # don't send msg to server and msg owner
    for socket in outputs:
        if socket != s:
            try :
                #print("try to broadcast ", message)
                socket.send(message.encode())
            except :
                # exit chat room
                socket.close()
                outputs.remove(socket)


def server_mode():
    #print("Server socket is start on port: ", results.port)

    try:

        while True:
            # Get read,writes error's sockets list
            read_sockets,write_sockets,error_sockets = select.select(connections,outputs,[])

            for s in read_sockets:

                # When a client connect to server that is server is readable
                if s == server_socket:
                    s_client, addr = server_socket.accept()
                    connections.append(s_client)
                    s_client.setblocking(0)
                    #print(addr)
                    #print("Client ", addr, "connected.")
                    msg = "Client "+ str(addr) + " entered the chat room."
                    # broadcast enter msg to all user in chat room
                    broadcast_data(s_client,msg)


                else:

                    data = s.recv(1024).decode()

                    if data:
                         #print("has rev",data)
                         if s not in outputs:
                            outputs.append(s)

                         #broadcast_data(s, str(addr) + ': ' + data)
                         print(data)
                         broadcast_data(s, data)
                    # when can not rev data(client has offline)

                    else:
                        msg = "Client "+ str(addr) + " is offline."
                        broadcast_data(s, msg)
                        if s in outputs:
                            outputs.remove(s)
                        s.close()
                        connections.remove(s)
                        continue




            for s in error_sockets:
                #print('handling exceptional condition for', s.getpeername()[0])
                connections.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()


    except EOFError:
        server_socket.close()
        sys.exit()
    except KeyboardInterrupt:
        server_socket.close()
        sys.exit()


    server_socket.close()

def server_mode2():
    conn, addr = server_socket.accept()
    try:
        trd_rev=threading.Thread(target=client_rev,args=(conn,))
        trd_rev.start()
        trd_send = threading.Thread(target=client_send,args=(conn,))
        trd_send.start()
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()



def client_rev(socket):
    try:
        while True:
            data = socket.recv(1024)
            if len(data) != 0:
                sys.stdout.write(data)
                sys.stdout.flush()
            else:
                socket.close()
                sys.exit()
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()


def client_send(socket):
    try:
        while True:
            #msg = input(">>:")
            msg = sys.stdin.readline()
            socket.send(msg)
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()



def client_mode(hostname):
    #host = hostname
    #port = int(results.port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to remote host
    s.connect((socket.gethostname(),int(results.port)))

    # Using thread to listen and send data at the same time
    try:
        trd_rev=threading.Thread(target=client_rev,args=(s,))
        trd_rev.start()
        trd_send = threading.Thread(target=client_send,args=(s,))
        trd_send.start()
    except EOFError:
        sys.exit()
    except KeyboardInterrupt:
        sys.exit()





if __name__ == "__main__":
    # Input connect to server socket
    connections = []
    # output socket list
    outputs = []

    # use para to select mode of this program
    # use -s start server mode
    # use -c start client mode
    # use -p to set TCP/IP port
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
        host = socket.gethostname()
        #print(host)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #server_socket.setblocking(False)
        server_socket.bind(("", int(results.port)))
        server_socket.listen(10)  # max client num
        connections.append(server_socket)
        server_mode2()

    # run a client
    elif results.hostname != None:
        hostname = results.hostname
        client_mode(hostname)

