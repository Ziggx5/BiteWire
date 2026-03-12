import socket
import threading
import json
import ssl

host = "192.168.1.7"
port = 50505

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile = "/home/ziggx/Documents/BitWire/server/server.crt", keyfile = "/home/ziggx/Documents/BitWire/server/server.key")

clients = []
users = {}

def send_message_to_clients(message):
    for client in clients[:]:
        try:
            client.send((json.dumps(message) + "\n").encode("utf-8"))
        except Exception as e:
            clients.remove(client)
            print(f"send message to clients {str(e)}")

def client_handler(client, address):
    logged_user = None
    buffer = ""
    while True:
        try:
            recv_data = client.recv(1024)
            print(recv_data)

            if not recv_data:
                break

            buffer += recv_data.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

            data = json.loads(recv_data.decode("utf-8"))
            if data["type"] == "register":
                username = data["username"]
                password = data["password"]
        
                if username in users:
                    send_json(client, {"type": "register", "status": "fail"})
                    
                else:
                    users[username] = password
                    send_json(client, {"type": "register", "status": "ok"})
                    
            elif data["type"] == "login":
                username = data["username"]
                password = data["password"]

                if users.get(username) == password:
                    logged_user = username
                    if client not in clients:
                        clients.append(client)
                    send_json(client, {"type": "login", "status": "ok"})
                else:
                    send_json(client, {"type": "login", "status": "fail"})

            elif data["type"] == "message":
                send_message_to_clients({"type": "message", "user": logged_user, "content": data['content']})
        except Exception as e:
            print(f"client handler {str(e)}")
        
    if client in clients:
        clients.remove(client)
    client.close()

def receive_connection():
    while True:
        client, address = server.accept()
        tls_connect = context.wrap_socket(client, server_side = True)
        thread = threading.Thread(target = client_handler, args = (tls_connect, address,))
        thread.start()

def send_json(client, data):
    client.send((json.dumps(data) + "\n").encode("utf-8"))

print("server running...")
receive_connection()