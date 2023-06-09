import subprocess
import os


def scaleImg(imageUrl):
    model_name = "RealESRGAN_x4plus_anime_6B"
    output_folder = "outputs"

    subprocess.run(
        [
            "python3",
            "inference_realesrgan.py",
            "-n",
            model_name,
            "-i",
            imageUrl,
            "-o",
            output_folder,
        ],
        shell=True,
    )

    output_path = os.path.join(output_folder, os.path.basename(imageUrl))
    return os.path.abspath(output_path)
