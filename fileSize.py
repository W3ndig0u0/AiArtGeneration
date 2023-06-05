import os
import math


def print_available_models(cache_dir):
    file_list = os.listdir(cache_dir)
    if file_list:
        models = []
        for file_name in file_list:
            file_path = os.path.join(cache_dir, file_name)
            if (
                os.path.isdir(file_path)
                or file_name.endswith(".safetensors")
                or file_name.endswith(".ctpk")
            ):
                file_size = (
                    get_folder_size(file_path)
                    if os.path.isdir(file_path)
                    else os.path.getsize(file_path)
                )
                model_info = {"name": file_name, "size": file_size}
                models.append(model_info)
        response = models
    else:
        response = "No models found in the cache directory."
    return response


def get_folder_size(folder_path):
    total_size = 0
    for path, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(path, file)
            total_size += os.path.getsize(file_path)
    return convert_size(total_size)


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    size = round(size_bytes / p, 1)
    return f"{size} {size_name[i]}"
