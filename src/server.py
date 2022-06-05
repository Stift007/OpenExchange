import socket
import select

HEADER_LENGTH = 10
IP = socket.gethostname()
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))

print(f"Running Cube '{__file__}' on {IP}:{PORT}...")
server_socket.listen()

sockets = [server_socket] 

clients = {}

def recv_message(client):
    try:
        message_header = client.recv(HEADER_LENGTH)

        if not len(message_header):
            return False

        message_length = int(message_header.decode("utf-8").strip())

        return {"header": message_header, "data": client.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(sockets, [], sockets)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_addr = server_socket.accept()

            user = recv_message(client_socket)

            if not user:
                continue

            sockets.append(client_socket)

            clients[client_socket] = user

            print(f"CONNECT SSTP 1/1 {user['data'].decode('utf-8')}@{client_addr[0]}:{client_addr[1]}")

        else:
            message = recv_message(notified_socket)

            if not message:
                print(f"CLOSE SSTP 1/1 {clients[notified_socket]['data'].decode('utf-8')}")
                sockets.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            print(f'RECV SSTP 1/1 {user["data"].decode("utf-8")} -M {message["data"].decode("utf-8")}')
            
            for client_socket in clients:
                # if client_socket != notified_socket:
                client_socket.send(user['header']+user['data']+message['header']+message["data"])

    for notified_socket in exception_sockets:
        sockets.remove(notified_socket)
        del clients[notified_socket]
        