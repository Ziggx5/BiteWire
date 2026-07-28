from platformdirs import user_data_dir
import os
import json

def app_directory():
    app_name = "BiteWire"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)

    return data_dir

def server_file():
    data_dir = app_directory()
    server_file_path = os.path.join(data_dir, "servers.json")

    return server_file_path

def server_icons_file():
    data_dir = app_directory()
    server_icons_folder_path = os.path.join(data_dir, "server_icons")
    os.makedirs(server_icons_folder_path, exist_ok = True)

    return server_icons_folder_path

def save_server_icon(image, server_name):
    data_dir = server_icons_file()
    image_path = os.path.join(data_dir, server_name + ".png")
    image.save(image_path)

def save_server_data(name, ip_address):
    server_file_path = server_file()
    data = {
        "name": name,
        "ip_address": ip_address,
        "user_count": 0
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

def update_user_count(ip_address, new_user_count):
    server_file_path = server_file()
    servers = []

    for server in server_loader():
        if server["ip_address"] == ip_address:
            server['user_count'] = new_user_count
        servers.append(server)

    with open (server_file_path, "w", encoding = "utf-8") as f:
        json.dump(servers, f, indent = 4)

def check_duplicate_server(ip_address):
    for server in server_loader():
        if server["ip_address"] == ip_address:
            return True

    return False