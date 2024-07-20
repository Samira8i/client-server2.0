import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
            else:
                break
        except Exception as e:
            print(f"Error receiving message: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 5555))

    login = input("Login: ")
    password = input("Password: ")

    prompt = client_socket.recv(1024).decode('utf-8')
    if prompt == "LOGIN:":
        client_socket.send(login.encode('utf-8'))

    prompt = client_socket.recv(1024).decode('utf-8')
    if prompt == "PASSWORD:":
        client_socket.send(password.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response to authentication: {response}")

    if response == "OK":
        print("Login successful!")
        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        try:
            while True:
                message = input()
                if message.lower() == 'exit':
                    client_socket.close()
                    break
                client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("Client is shutting down.")
            client_socket.close()
            receive_thread.join()
    else:
        print("Login failed! Invalid credentials.")
        client_socket.close()

if __name__ == "__main__":
    main()

