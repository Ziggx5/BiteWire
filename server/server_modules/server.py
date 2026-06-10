import socket
import threading
import json
import ssl
import sqlite3
import time
import os
import base64
from datetime import datetime
from server_modules.data_manipulation import files_check, database_files, profile_pictures_file
from PySide6.QtCore import Signal, QObject
import bcrypt
import struct

class Client:
    def __init__(self, conn, address):
        self.conn = conn
        self.address = address
        self.username = None
        self.buffer = ""
        self.last_pong = None

    def recvall(self, length):
        data = b""

        while len(data) < length:
            packet = self.conn.recv(length - len(data))

            if not packet:
                return None
            
            data += packet
        
        return data

    def receive_json_message(self):
        raw_length = self.recvall(4)

        if not raw_length:
            return None

        length = struct.unpack("!I", raw_length)[0]

        data = self.recvall(length)

        if not data:
            return None

        return json.loads(data.decode("utf-8"))
    
    def send(self, data):
        try:
            message = json.dumps(data).encode("utf-8")
            length = struct.pack("!I", len(message))
            self.conn.send(length + message)
        except Exception as e:
            print(e)

class ChatServer(QObject):
    uptime_signal = Signal(int, int, int)

    def __init__(self):
        super().__init__()

        self.host = "0.0.0.0"
        self.port = 50505
        self.clients = []
        self.stop_event = threading.Event()
        self.clients_lock = threading.Lock()

        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

        self.certfile = None
        self.keyfile = None
        self.database = None

        self.load_files()
        self.users_database_path, self.messages_database_path = database_files()
        self.profile_pictures_path = profile_pictures_file()

    def load_files(self):
        for file_path in files_check():
            if file_path.endswith(".crt"):
                self.certfile = file_path
            elif file_path.endswith(".key"):
                self.keyfile = file_path
            elif file_path.endswith(".db"):
                self.database = file_path

    def init_database(self):
        conn = sqlite3.connect(self.users_database_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                profile_picture TEXT
            )
        """)
        conn.commit()
        conn.close()

        conn = sqlite3.connect(self.messages_database_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT,
                content TEXT,
                created_at TEXT
            )
        """)

        conn.commit()
        conn.close()

    def register_user(self, username, password, profile_picture):
        conn = sqlite3.connect(self.users_database_path)
        cursor = conn.cursor()

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        decode_profile_picture = base64.b64decode(profile_picture)
        image_path = f"{self.profile_pictures_path}/{username}.jpg"
        with open (image_path, "wb") as f:
            f.write(decode_profile_picture)

        try:
            cursor.execute(
                "INSERT INTO users (username, password, profile_picture) VALUES (?, ?, ?)",
                (username, hashed_password, image_path)
            )
            conn.commit()
            return True

        except sqlite3.IntegrityError:
            return False

        finally:
            conn.close()
    
    def login_user(self, username, password):
        conn = sqlite3.connect(self.users_database_path)
        cursor = conn.cursor()

        try:
            cursor.execute(
                "SELECT password FROM users WHERE username = ?",
                (username,)
            )

            result = cursor.fetchone()

            if not result:
                return False

            stored_hash = result[0].encode("utf-8")
            return bcrypt.checkpw(password.encode("utf-8"), stored_hash)

        finally:
            conn.close()

    def process_message(self, client, data):
        message_type = data.get("type")

        if message_type == "register":
            username = data.get("username")
            password = data.get("password")
            profile_picture = data.get("profile_picture")

            if not isinstance(username, str) or not isinstance(password, str):
                return

            if self.register_user(username, password, profile_picture):
                client.send({"type": "register", "status": "ok"})
                self.send_users_list_all_clients()

            else:
                client.send({"type": "register", "status": "fail"})

        elif message_type == "login":
            username = data.get("username")
            password = data.get("password")

            if not isinstance(username, str) or not isinstance(password, str):
                return

            if self.login_user(username, password):
                client.username = username
                client.send({"type": "login", "status": "ok"})
                self.add_client(client)
                self.send_users_list_all_clients()
                self.send_profile_picture(client)
                self.send_message_history(client)
            else:
                client.send({"type": "login", "status": "fail"})
        
        elif message_type == "message":
            if not client.username:
                return

            content = data.get("content")

            if not isinstance(content, str):
                return

            if len(content) > 300:
                return

            current_time = datetime.now().strftime("%l:%M %p, %m/%d/%y")

            self.save_message_to_database(client.username, content, current_time)
            self.broadcast({
                "type": "message",
                "user": client.username,
                "content": content,
                "time": current_time
            })

        elif message_type == "pong":
            client.last_pong = time.time()
        
        elif message_type == "message_history":
            content = data.get("content")
            
            self.send_message_history(client, content)

        else:
            self.remove_client(client)
            self.safe_client_close(client)

    def client_handler(self, client):
        while True:
            try:
                data = client.receive_json_message()

                if not data:
                    break

                if not isinstance(data, dict):
                    break

                self.process_message(client, data)

            except Exception as e:
                print(e)
                break
        
        self.remove_client(client)
        self.safe_client_close(client)

    def start(self):
        if not self.certfile or not self.keyfile:
            return

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        
        self.stop_event.clear()
        self.context.load_cert_chain(self.certfile, self.keyfile)

        threading.Thread(target = self.server_uptime, daemon = True).start()
        threading.Thread(target = self.ping_client, daemon = True).start()

        self.init_database()

        while not self.stop_event.is_set():
            try:
                self.server.settimeout(1.0)
                conn, address = self.server.accept()
            except socket.timeout:
                continue
            except OSError:
                break

            try:
                tls_conn = self.context.wrap_socket(conn, server_side = True)
                client = Client(tls_conn, address)
            except Exception as e:
                print(e)
                conn.close()
                continue

            threading.Thread(target = self.client_handler, args = (client,), daemon = True).start()

    def stop(self):
        self.stop_event.set()

        self.disconnect_all_clients()
        try:
            self.server.close()
        except:
            pass

    def remove_client(self, client):
        with self.clients_lock:
            if client in self.clients:
                self.clients.remove(client)
        self.send_users_list_all_clients()

    def add_client(self, client):
        with self.clients_lock:
            if client not in self.clients:
                self.clients.append(client)

    def disconnect_all_clients(self):
        self.broadcast({"type": "server_status", "status": "Server has been closed."})
            
        with self.clients_lock:
            copy_clients = self.clients[:]
            self.clients.clear()

        for client in copy_clients:
            try:
                client.conn.shutdown(socket.SHUT_RDWR)
            except:
                pass

            try:
                client.conn.close()
            except:
                pass

    def broadcast(self, message):
        with self.clients_lock:
            for client in self.clients[:]:
                try:
                    client.send(message)
                except:
                    self.clients.remove(client)

    def send_users_list_all_clients(self):
        conn = sqlite3.connect(self.users_database_path)
        cursor = conn.cursor()
        online_users = []
        users = []
        
        try:
            cursor.execute("SELECT username FROM users")
            result = cursor.fetchall()

            for client in self.clients:
                if client.username:
                    online_users.append(client.username)
                        
            for (user,) in result:
                users.append({"username": user, "status": user in online_users})

            self.broadcast({"type": "users_list", "content": users})
        finally:
            conn.close()

    def server_uptime(self):
        start_time = time.time()

        while not self.stop_event.is_set():
            elapsed_time = int(time.time() - start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            self.uptime_signal.emit(hours, minutes, seconds)
            time.sleep(1)

    def save_message_to_database(self, username, content, time):
        conn = sqlite3.connect(self.messages_database_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO messages (sender, content, created_at)
            VALUES (?, ?, ?)
        """, (username, content, time))

        conn.commit()
        conn.close()

    def ping_client(self):
        while not self.stop_event.is_set():
            time.sleep(15)
            self.broadcast({"type": "ping"})

            with self.clients_lock:
                clients_copy = self.clients[:]

            for client in clients_copy:
                if not client.last_pong:
                    continue

                if time.time() - client.last_pong > 30:
                    self.remove_client(client)
                    self.safe_client_close(client)

    def send_message_history(self, client, old_id = None):
        conn = sqlite3.connect(self.messages_database_path)
        cursor = conn.cursor()

        if old_id:
            cursor.execute("""
            SELECT sender, content, created_at, id
            FROM (
                SELECT sender, content, created_at, id
                FROM messages
                WHERE id < ?
                ORDER BY id DESC            
                LIMIT 20         
            )
            ORDER BY id ASC
            """, (old_id,))

            result = cursor.fetchall()

            messages = []

            for message in result:
                messages.append({"id": message[3], "user": message[0], "content": message[1], "time": message[2]})
            
            client.send({"type": "message_history", "content": messages})

        else:
            cursor.execute("""
                SELECT sender, content, created_at, id
                FROM (
	                SELECT sender, content, created_at, id
	                FROM messages
	                ORDER BY id DESC
	                LIMIT 20
                )
                ORDER BY id ASC
            """)

            result = cursor.fetchall()

            messages = []

            for message in result:
                messages.append({"id": message[3], "user": message[0], "content": message[1], "time": message[2]})
            
            client.send({"type": "first_message_history", "content": messages})

    def send_profile_picture(self, client):
        data = []
        conn = sqlite3.connect(self.users_database_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT profile_picture, username FROM users
        """)

        result = cursor.fetchall()

        for picture_path, username in result:
            with open(picture_path, "rb") as f:
                image_bytes = f.read()

            encoded_image_bytes = base64.b64encode(image_bytes).decode("utf-8")

            data.append({"username": username, "image_bytes": encoded_image_bytes})

        client.send({"type": "profile_picture_data", "content": data})

    def safe_client_close(self, client):
        try:
            client.conn.shutdown(socket.SHUT_RDWR)
        except:
            pass
        
        try:
            client.conn.close()
        except:
            pass