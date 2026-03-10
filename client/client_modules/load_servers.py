import json
from platformdirs import user_data_dir
import os
from client_modules.data_manipulation import local_file_path

def server_loader():
    file_path = local_file_path()

    if not os.path.exists(file_path):
        return []

    with open (file_path, "r") as f:
        server_list = json.load(f)
    
    return server_list