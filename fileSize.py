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
                
                # Define an image path for each model (can be based on model name or another strategy)
                model_image = get_model_image(file_name)  # Custom function to get model image
                
                model_info = {
                    "name": file_name,
                    "size": file_size,
                    "image": model_image,  # Add the image path to model info
                }
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


def get_model_image(model_name):
    """
    Return a different image path for each model based on the model name.
    """
    model_image_map = {
        "models--JingAnimeV2": "/GeneratedImg/196.png",  # Image for JingAnimeV2
        "models--stablediffusionapi--realistic-vision-v51": "/GeneratedImg/20241103_231916.png",  # Image for Realistic Vision V51
    }

    # Default to a generic image if model name is not found
    return model_image_map.get(model_name, "/GeneratedImg/211.png")
