from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from CLI chaT! Now type your name and press enter! ", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_commands(command):
    command_args = command.split(" ")
    if command_args[0].lower() == 'list':
        print(clients)


def handle_client(client):
    global clients
    client_names = ""
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        if name == 'admin':
            admin_welcome = "Enter your password"
            client.send(bytes(admin_welcome, "utf8"))
            password = client.recv(BUFSIZ).decode("utf8")
            if password == 'admin':
                admin_welcome2 = "Welcome admin! You can either list the clients or kick them out"
                client.send(bytes(admin_welcome2, "utf8"))
                while True:
                    msg = client.recv(BUFSIZ).decode("utf8")
                    if msg == 'list':
                        client_names = ""
                        for i in clients:
                            client_names = client_names + ",\n" + str(i)
                            client.send(bytes(client_names, "utf8"))
                    elif msg.split(" ")[0] == 'kick':
                         try:
                            kick_out = msg.split(" ")[1]
                            for sock in clients:
                                if sock == kick_out:
                                    msg = "disconnect"
                                    sock.send(bytes("utf8") + msg)
                         except:
                             error_message = "Please provide a client address or name to kick out"
                             client.send(bytes(error_message, "utf8"))
        else:
            welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
            client.send(bytes(welcome, "utf8"))
            msg = "%s has joined the chat!" % name
            print(msg)
            broadcast(bytes(msg, "utf8"))
            clients[client] = name

            while True:
                msg = client.recv(BUFSIZ)
                if msg != bytes("{quit}", "utf8"):
                    broadcast(msg, name + ": ")
                else:
                    client.send(bytes("{quit}", "utf8"))
                    client.close()
                    del clients[client]
                    broadcast(bytes("%s has left the chat." % name, "utf8"))
                    break
    except ConnectionResetError:
        print("%s has left the chat" % name)


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


global clients

clients = {}
addresses = {}

HOST = '0.0.0.0'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
