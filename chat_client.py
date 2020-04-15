from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == 'disconnect':
                client_socket.close()
            print(msg)
        except OSError:
            break


def establish_connection():
    try:
        HOST = input('Enter host: ')
        PORT = input('Enter port: ')

        if not HOST:
            HOST = 'localhost'
        else:
            HOST = str(HOST)

        if not PORT:
            PORT = 33000
        else:
            PORT = int(PORT)

        ADDR = (HOST, PORT)

        global client_socket
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect(ADDR)

        receive_thread = Thread(target=receive)
        receive_thread.start()

    except ConnectionRefusedError:
        print("The server you are trying to connect to is currently unavailable. "
              "Please recheck your host and port, or try again later.")
        establish_connection()


def send(event=None):
    try:
        msg = input(" ")
        client_socket.send(bytes(msg, "utf8"))
        if msg == "{quit}":
            client_socket.send(bytes("Client has left the chat", "utf8"))
            client_socket.close()
    except OSError:
        print("You are now disconnected. Please restart the app to join another server")


BUFSIZ = 1024
establish_connection()

while True:
    send()
