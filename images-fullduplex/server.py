import socket
import threading
import subprocess
import os

def send_image(sock, image_path, prompt_prefix):
    if not os.path.isfile(image_path):
        print(f"\n[-] Error: File '{image_path}' does not exist.")
        print(f"{prompt_prefix}", end="")
        return

    filename = os.path.basename(image_path)
    filesize = os.path.getsize(image_path)

    
    header = f"img_send:{filename}:{filesize}"
    sock.sendall(header.encode('utf-8'))

    
    with open(image_path, 'rb') as f:
        while chunk := f.read(4096):
            sock.sendall(chunk)

    print(f"[+] Sent image '{filename}' ({filesize} bytes).")

def receive_messages(sock, role_name):
    prompt_prefix = f"[{role_name}]: "
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                break
            
            message = data.decode('utf-8', errors='ignore')

            
            if message.startswith("img_send:"):
                parts = message.split(":", 2)
                filename = "received_" + parts[1]
                filesize = int(parts[2])
                print(f"\n[+] Receiving image '{filename}' ({filesize} bytes)...")

                received_bytes = 0
                with open(filename, 'wb') as f:
                    while received_bytes < filesize:
                        chunk = sock.recv(min(4096, filesize - received_bytes))
                        if not chunk:
                            break
                        f.write(chunk)
                        received_bytes += len(chunk)

                print(f"[+] Image saved as '{filename}'.\n{prompt_prefix}", end="")

            
            elif message.startswith("cmd:"):
                command = message[4:].strip()
                print(f"\n[Executing Command]: {command}")
                try:
                    output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
                    if not output:
                        output = "Command executed successfully (no output)."
                except subprocess.CalledProcessError as e:
                    output = f"Command failed with error:\n{e.output}"
                
                sock.sendall(f"\n--- {role_name} Output ---\n{output}\n---------------------".encode('utf-8'))

            
            else:
                peer_label = "Client" if role_name == "Server" else "Server"
                print(f"\n[{peer_label}]: {message}\n{prompt_prefix}", end="")

        except Exception as e:
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
    print("[*] Options:\n  - Chat: Type regular text\n  - Command: 'cmd: <command>'\n  - Image: 'img: <path_to_image>'")

    recv_thread = threading.Thread(target=receive_messages, args=(conn, "Server"))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            msg = input("[Server]: ")
            if msg.lower() == 'quit':
                break
            if msg.startswith("img:"):
                send_image(conn, msg[4:].strip(), "[Server]: ")
            else:
                conn.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break

    conn.close()
    server.close()

if __name__ == '__main__':
    main()
