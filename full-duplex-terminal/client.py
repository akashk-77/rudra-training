import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[Server]: {message}\n[You]: ", end="")
        except:
            break

def main():
    host = '127.0.0.1'
    port = 65432

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print("[+] Connected to server.")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return

    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            msg = input("[You]: ")
            if msg.lower() == 'quit':
                break
            client.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break

    client.close()

if __name__ == '__main__':
    main()
