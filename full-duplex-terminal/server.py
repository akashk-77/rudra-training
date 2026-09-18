import socket
import threading
import subprocess

def receive_messages(sock):
    while True:
        try:
            message = sock.recv(4096).decode('utf-8')
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
                
                sock.sendall(f"\n--- Server Output ---\n{output}\n---------------------".encode('utf-8'))
            else:
                print(f"\n[Client]: {message}\n[Server]: ", end="")
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
    print("[*] Type text to chat, or 'cmd: <command>' to run remote commands on Client.")

    recv_thread = threading.Thread(target=receive_messages, args=(conn,))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            msg = input("[Server]: ")
            if msg.lower() == 'quit':
                break
            conn.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break

    conn.close()
    server.close()

if __name__ == '__main__':
    main()
