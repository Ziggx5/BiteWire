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
        #split_file_path = os.path.splitext()
        data_file_path = local_data_file()
        file_name = os.path.basename(file_path)
        extension = os.path.splitext(file_name)[1]
        print(extension)
        destination_path = os.path.join(data_file_path, file_name)
        print(destination_path)
        
        if not os.path.exists(destination_path):
            shutil.copy(file_path, destination_path)

        return destination_path, extension