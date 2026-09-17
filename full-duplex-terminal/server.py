import socket
import threading

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"\n[Client]: {message}\n[You]: ", end="")
        except:
            break

def main():
    host = '127.0.0.1'
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[*] Server listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"[+] Connected by {addr}")

    recv_thread = threading.Thread(target=receive_messages, args=(conn,))
    recv_thread.daemon = True
    recv_thread.start()

    
    while True:
        try:
            msg = input("[You]: ")
            if msg.lower() == 'quit':
                break
            conn.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break

    conn.close()
    server.close()

if __name__ == '__main__':
    main()
