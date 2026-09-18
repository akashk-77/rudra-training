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
                
                sock.sendall(f"\n--- Client Output ---\n{output}\n---------------------".encode('utf-8'))
            else:
                print(f"\n[Server]: {message}\n[Client]: ", end="")
        except:
            break

def main():
    host = '127.0.0.1'
    port = 65432

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print("[+] Connected to Server.")
        print("[*] Type text to chat, or 'cmd: <command>' to run remote commands on Server.")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return

    recv_thread = threading.Thread(target=receive_messages, args=(client,))
    recv_thread.daemon = True
    recv_thread.start()

    while True:
        try:
            msg = input("[Client]: ")
            if msg.lower() == 'quit':
                break
            client.sendall(msg.encode('utf-8'))
        except KeyboardInterrupt:
            break

    client.close()

if __name__ == '__main__':
    main()
