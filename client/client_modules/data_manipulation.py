from platformdirs import user_data_dir
import os
import json

def local_file_path():
    app_name = "BitWire"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)
    file_path = os.path.join(data_dir, "servers.json")

    return file_path

def save_server_data(name, ip_address):
    file_path = local_file_path()
    data = {
        "name": name,
        "ip_address": ip_address
    }
    servers = []

    if os.path.exists(file_path):
        with open (file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []

    servers.append(data)
        
    with open (file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)
    
def delete_server(ip_address):
    file_path = local_file_path()
    servers = []

    if os.path.exists(file_path):
        with open (file_path, "r", encoding = "utf-8") as f:
            try:
                servers = json.load(f)
            except json.JSONDecodeError:
                servers = []
        
    for i, server in enumerate(servers):
        if server["ip_address"] == ip_address:
            servers.pop(i)
    
    with open (file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)
        
def save_identity_data(username, password):
    print(username)
    print(password)