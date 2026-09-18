import socket
import threading
import subprocess

def handle_client(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if not message:
                break
            
            if message.startswith("cmd:"):
                command = message[4:].strip()
                print(f"\n[Executing Command]: {command}")
                
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    if not output:
                        output = "Command executed successfully (no output)."
                except subprocess.CalledProcessError as e:
                    output = f"Command failed with error:\n{e.output}"
                
                sock.sendall(f"\n--- Command Output ---\n{output}\n----------------------".encode('utf-8'))
            else:
                print(f"\n[Client]: {message}\n[You]: ", end="")

        except:
            break

def main():
    host = '127.0.0.1'
    port = 65432

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)
    print(f"[*] Command-Enabled Server listening on {host}:{port}...")

    conn, addr = server.accept()
    print(f"[+] Connected by {addr}")

    recv_thread = threading.Thread(target=handle_client, args=(conn,))
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
