import socket
import threading
import json
import ssl
from PySide6.QtCore import QObject, Signal
import struct

class ChatHandler(QObject):
    message_received = Signal(str, str, str, str)
    history_message_received = Signal(list)
    first_history_message_received = Signal(str, str, str, str, int)
    users_received = Signal(list)
    server_status = Signal(str)
    users_count_signal = Signal(str)
    server_icon_signal = Signal(str)

    def __init__(self, profile_cache = None):
        super().__init__()

        self.client = None
        self.running = False
        self.context = ssl.create_default_context()
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE
        self.profile_cache = profile_cache

    def connect(self, ip_address, port = 50505):
        raw_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        raw_socket.settimeout(2)
        tls_socket = self.context.wrap_socket(raw_socket, server_hostname = ip_address)
        tls_socket.connect((ip_address, port))
        self.client = tls_socket

    def recvall(self, length):
        data = b""

        while len(data) < length:
            packet = self.client.recv(length - len(data))

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


    def receive_messages(self):
        while self.running and self.client:
            try:
                message = self.receive_json_message()

                if not message:
                    break

                print(message['type'])
                
                message_type = message.get("type")
                if message_type == "message":
                    sender_type = message['sender_type']
                    username = message['user']
                    content = message['content']
                    time = message['time']
                    self.message_received.emit(sender_type, username, content, time)
                    
                elif message_type == "users_list":
                    users = message['content']
                    self.users_received.emit(users)
                        
                elif message_type == "server_status":
                    self.server_status.emit(message['status'])
                    self.handle_disconnect()
                    
                elif message_type == "ping":
                    self.send_json_message({"type": "pong"})
                
                elif message_type == "first_message_history":
                    for content in message['content']:
                        self.first_history_message_received.emit(content['sender_type'], content['sender_username'], content['content'], content['time'], content['id'])
                    
                elif message_type == "message_history":
                    self.history_message_received.emit(message['content'])
                    
                elif message_type == "profile_picture_data":
                    self.profile_cache.save(message['content'])
                
                elif message_type == "users_count":
                    self.users_count_signal.emit(message['content'])

                elif message_type == "server_icon":
                    self.server_icon_signal.emit(message['content'])

            except socket.timeout:
                continue
            except Exception as e:
                if not self.running:
                    return
                print(str(e))
                self.handle_disconnect()
                break
    
    def send_json_message(self, message):
        if not self.client:
            return
        try:
            data = json.dumps(message).encode("utf-8")
            length = struct.pack("!I", len(data))
            self.client.sendall(length + data)
        except:
            self.handle_disconnect()

    def register(self, username, password, ip_address, encoded_profile_picture):
        try:
            self.connect(ip_address)
            self.send_json_message({
                "type": "register",
                "username": username,
                "password": password,
                "profile_picture": encoded_profile_picture
            })
            response = self.receive_json_message()
            
        except Exception as e:
            self.handle_disconnect()
            return {"type": "error", "message": str(e)}

        self.handle_disconnect()
        return response

    def login(self, username, password, ip_address):
        try:
            self.connect(ip_address)
            self.send_json_message({
                "type": "login",
                "username": username,
                "password": password
            })
            response = self.receive_json_message()
            
            if response["status"] == "ok":
                self.running = True
                threading.Thread(target = self.receive_messages, daemon = True).start()
            else:
                self.handle_disconnect()

        except socket.timeout:
            return {"type": "error", "message": "Server not responding."}
        except Exception as e:
            return {"type": "error", "message": str(e)}
            self.handle_disconnect()

        return response

    def send_message(self, message):
        self.send_json_message({
            "type": "message",
            "content": message
        })
    
    def handle_disconnect(self):
        if not self.client:
            return
            
        self.running = False

        client = self.client
        self.client = None

        try:
            client.shutdown(socket.SHUT_RDWR)
        except:
            pass

        try:
            client.close()
        except:
            pass

    def get_profile_pictures(self, username):
        self.send_json_message({"type": "get_profile_picture", "username": username})