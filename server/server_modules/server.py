import socket
import threading
import json
import ssl
import sqlite3
import time
from server_modules.data_manipulation import database_file, files_check

host = "192.168.1.7"
port = 50505

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

all_files = files_check()
for file_path in all_files:
    if file_path.endswith(".crt"):
        certfile = file_path
    elif file_path.endswith(".key"):
        keyfile = file_path

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

clients = []

stop_event = threading.Event()

def init_database():
    database_path = database_file()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    """)
    conn.commit()
    conn.close()

def send_message_to_clients(message):
    for client in clients[:]:
        try:
            client.send((json.dumps(message) + "\n").encode("utf-8"))
        except Exception as e:
            clients.remove(client)
            print({str(e)})

def client_handler(client, address):
    logged_user = None
    buffer = ""
    while True:
        try:
            recv_data = client.recv(1024)

            if not recv_data:
                break

            buffer += recv_data.decode("utf-8")
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

                data = json.loads(line)
                if data["type"] == "register":
                    username = data["username"]
                    password = data["password"]

                    if register_user(username, password):
                        send_json(client, {"type": "register", "status": "ok"})
                    else:
                        send_json(client, {"type": "register", "status": "fail"})
         
                elif data["type"] == "login":
                    username = data["username"]
                    password = data["password"]

                    if login_user(username, password):
                        send_json(client, {"type": "login", "status": "ok"})
                        logged_user = username
                        if client not in clients:
                            clients.append(client)
                    else:
                        send_json(client, {"type": "login", "status": "fail"})

                elif data["type"] == "message":
                    send_message_to_clients({"type": "message", "user": logged_user, "content": data['content']})
        except Exception as e:
            print(str(e))
        
    if client in clients:
        clients.remove(client)
    client.close()

def receive_connection(callback):
    if not certfile or not keyfile:
        return
    stop_event.clear()
    context.load_cert_chain(certfile = certfile, keyfile = keyfile)
    print("server running...")
    threading.Thread(target = server_uptime, args = (stop_event, callback,), daemon = True).start()
    init_database()
    while not stop_event.is_set():
        try:
            server.settimeout(1.0)
            client, address = server.accept()
        except socket.timeout:
            continue
        except OSError:
            break

        tls_connect = context.wrap_socket(client, server_side = True)
        thread = threading.Thread(target = client_handler, args = (tls_connect, address,))
        thread.start()

def send_json(client, data):
    client.send((json.dumps(data) + "\n").encode("utf-8"))

def register_user(username, password):
    database_path = database_file()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError as e:
        print(f"str{e}")
        return False
    finally:
        conn.close()

def login_user(username, password):
    database_path = database_file()
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )
    
        result = cursor.fetchone()
        conn.close()

        if result and result[0] == password:
            return True

        return False

    except Exception as e:
        print(f"str{e}")

def start_receive_connection_thread(callback):
    threading.Thread(target = receive_connection, args = (callback,), daemon = True).start()

def stop_receive_connection_thread():
    print("Stopping server")
    stop_event.set()
    server.close()

def server_uptime(stop_event, callback):
    start_time = time.time()
    while not stop_event.is_set():
        end_time = time.time()
        elapsed_time = int(end_time) - int(start_time)
        print(elapsed_time)

        callback(elapsed_time)
        time.sleep(1)