from platformdirs import user_data_dir
import os
import json
from cryptography.fernet import Fernet
import base64

def create_local_file():
    app_name = "BiteWire"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)

    return data_dir

def server_file():
    data_dir = create_local_file()
    server_file_path = os.path.join(data_dir, "servers.json")

    return server_file_path

def save_server_data(name, ip_address):
    server_file_path = server_file()
    data = {
        "name": name,
        "ip_address": ip_address
    }
    servers = []

    if os.path.exists(server_file_path):
        with open (server_file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []

    servers.append(data)
        
    with open (server_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)
    
def delete_server(ip_address):
    server_file_path = server_file()
    servers = []

    if os.path.exists(server_file_path):
        with open (server_file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []
        
    for i, server in enumerate(servers):
        if server["ip_address"] == ip_address:
            servers.pop(i)
    
    with open (server_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)

def server_loader():
    file_path = server_file()

    if not os.path.exists(file_path):
        return []

    with open (file_path, "r") as f:
        server_list = json.load(f)
    
    return server_list