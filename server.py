import socket
import threading

users = {
    'samira': '1207',
    'rob': 'qwerty',
    #ну сюда любой пароль/логин, чтоюы запустить нужно ввести что-то из эт
}

clients = []


def handle_client(client_socket, client_address):
    try:
        while True:
            client_socket.send("LOGIN:".encode('utf-8'))
            login = client_socket.recv(1024).decode('utf-8')
            print(f"Received login: {login}")

            client_socket.send("PASSWORD:".encode('utf-8'))
            password = client_socket.recv(1024).decode('utf-8')
            print(f"Received password for {login}: {password}")

            if login in users and users[login] == password:
                client_socket.send("OK".encode('utf-8'))
                break
            else:
                client_socket.send("INVALID".encode('utf-8'))

        welcome_message = f"{login} has joined the chat!"
        broadcast(welcome_message, client_socket)
        print(welcome_message)

        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                broadcast(f"{login}: {message}", client_socket)
                print(f"{login}: {message}")
            else:
                break
    except Exception as e:
        print(f"Client {client_address} disconnected. {e}")
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()


def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error broadcasting message: {e}")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5555))
    server.listen(5)
    print("Server started on port 5555")

    try:
        while True:
            client_socket, client_address = server.accept()
            clients.append(client_socket)
            print(f"New connection from {client_address}")
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.daemon = True  # Установить поток как daemon
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
        server.close()


if __name__ == "__main__":
    main()
