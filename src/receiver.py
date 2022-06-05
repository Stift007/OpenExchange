import errno
import sys
from PyQt5.QtWidgets import QListWidget


qtmaster = None

running = True
HEADER_LENGTH = 10
client_socket = None


def receive_messages():
    while running:
        try:
            while True:
                username_header = client_socket.recv(HEADER_LENGTH)
                if not len(username_header):
                    print("Cube closed by Administrator")
                    sys.exit()
                username_len = int(username_header.decode('utf-8').strip())
                username = client_socket.recv(username_len).decode('utf-8')
                message_header = client_socket.recv(HEADER_LENGTH)
                message_len = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_len).decode('utf-8')

                print(username)
                qtmaster.listView.addItem(f'{username} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                qtmaster.listView.addItem("Reading Error: "+str(e))
                print("Reading Error: "+str(e))
            
        
        except Exception as e:
            qtmaster.listView.addItem('General Error: '+ str(e))
            sys.exit(-1)
            