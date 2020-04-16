from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

servers = {
    "asia": "35.198.233.187",
    "europe": "35.189.251.210",
    "america": "35.222.202.92",
    "oceania": "34.87.244.242"
}


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if msg == 'disconnect':
                client_socket.close()
            else:
                print(msg)
        except OSError:
            break


def establish_connection():
    try:
        print("Welcome! Choose between AMERICA, EUROPE, ASIA and OCEANIA servers")
        PORT = 33000
        SERVER = input('Enter server name: ').lower()
        if SERVER != 'asia' and SERVER != 'europe' and SERVER != 'america' and SERVER != 'oceania':
            print("You have entered an invalid server name. You have now been assigned the AMERICA server by default")
            SERVER = 'america'

        HOST = servers[SERVER]
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
