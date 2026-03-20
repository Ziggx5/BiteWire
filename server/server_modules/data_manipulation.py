from platformdirs import user_data_dir
import os
import shutil

def local_data_file():
    app_name = "Bitwire_server"
    data_dir = user_data_dir(app_name)
    os.makedirs(data_dir, exist_ok = True)

    return data_dir

def copy_to_data_dir(file_path):
    if file_path:
        data_file_path = local_data_file()
        file_name = os.path.basename(file_path)
        destination_path = os.path.join(data_file_path, file_name)

        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)

        return destination_path

def database_file():
    data_dir = local_data_file()
    database_path = os.path.join(data_dir, "users.db")

    return database_path

def files_check():
    data_dir = local_data_file()
    all_files = os.listdir(data_dir)

    files = []

    for item in all_files:
        file_path = os.path.join(data_dir, item)
        files.append(file_path)
    
    return files