from platformdirs import user_data_dir
import os
import json
import ssl
from datetime import datetime

def local_data_file():
    app_name = "BiteWire_Server"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)

    return data_dir

def database_files():
    data_dir = local_data_file()
    users_database_path = os.path.join(data_dir, "users.db")
    messages_database_path = os.path.join(data_dir, "messages.db")

    return users_database_path, messages_database_path

def files_check():
    data_dir = local_data_file()
    all_files = os.listdir(data_dir)

    files = []

    for item in all_files:
        file_path = os.path.join(data_dir, item)
        files.append(file_path)
    
    return files

def profile_pictures_file():
    data_dir = local_data_file()
    path = f"{data_dir}/profile_pictures"
    os.makedirs(path, exist_ok = True)

    return path

def validate_certificate():
    data_dir = local_data_file()
    cert = ssl._ssl._test_decode_cert(f"{data_dir}/server.crt")
    cert_issued = cert['notAfter']
    date_now = datetime.now()
    expiry_date = datetime.strptime(cert_issued, "%b %d %H:%M:%S %Y %Z")
    remaining_days = (expiry_date - date_now).days

    return str(expiry_date), str(remaining_days), cert_issued