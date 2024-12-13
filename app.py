from flask import Flask, render_template, request, jsonify, send_from_directory
from artGeneration import AnimeArtist
from safetensors import safe_open
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from fileSize import print_available_models
from upscale import scaleImg
from randomPrompt import prompt
import os
import json
import subprocess
from flask import send_file


app = Flask(__name__, static_url_path="/static", static_folder="static")
anime_artist = AnimeArtist()
randomPrompt = prompt()
image_folder = "GeneratedImg/"
cache_dir = "artModel/"

ACTIVE_MODEL_FILE = "active_model.txt"
vae_name = "stabilityai/sd-vae-ft-mse"
# vae_name = "/kl-f8-anime.ckpt"
#vae_name = "madebyollin/sdxl-vae-fp16-fix"

@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.json["user_input"]
    return jsonify({"response": response})


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/art")
def art():
    return render_template("art.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


@app.route("/upscale")
def upscale():
    image_url = request.args.get("image")
    return render_template("upscale.html", image_url=image_url)


@app.route("/upscale_image")
def upscale_image():
    image_url = request.args.get("image")
    upscaled_image_path = scaleImg(image_url)
    print(upscaled_image_path)
    if upscaled_image_path is not None:
        return send_file(upscaled_image_path, mimetype="image/png")
    else:
        return "Failed to upscale the image."


@app.route("/downloadModel", methods=["POST"])
def downloadModel():
    data = request.get_json()
    modelName = data.get("labelText")
    model = StableDiffusionPipeline.from_pretrained(modelName, cache_dir=cache_dir)
    set_active_model(model)
    return jsonify({"message": modelName})


@app.route("/gallery")
def gallery():
    image_files = [
        filename
        for filename in os.listdir(image_folder)
        if filename.endswith((".jpg", ".jpeg", ".png"))
    ]
    return render_template("gallery.html", image_files=image_files)


@app.route("/getImages")
def get_images():
    image_files = sorted(
        [
            filename
            for filename in os.listdir(image_folder)
            if filename.endswith((".jpg", ".jpeg", ".png"))
        ]
    )
    return jsonify({"imageFiles": image_files})


@app.route("/GeneratedImg/<path:path>")
def send_img(path):
    return send_from_directory(image_folder, path)


@app.route("/generate_art", methods=["POST"])
def generate_art():
    prompt = request.json["prompt"]
    negativePrompt = request.json.get("negativePrompt", "")
    num_inference_steps = int(request.json["num_inference_steps"])
    eta = float(request.json["eta"])
    guidance_scale = int(request.json["guidance_scale"])
    width = int(request.json.get("width", 640))
    height = int(request.json.get("height", 360))
    batch_size = int(request.json.get("batch_size", 1))
    seed = int(request.json.get("seed", -1))

    initial_generation = request.json.get("initial_generation", False)
    save_folder = "GeneratedImg/"

    img_folder, file_name = anime_artist.generate_art(
        prompt,
        width,
        height,
        num_inference_steps,
        eta,
        negativePrompt,
        guidance_scale,
        save_folder,
        seed,
        batch_size,
        get_active_model(),
        vae_name,
        initial_generation,
    )


    img_folder = f"{img_folder}"
    file_name = f"{file_name}.png"

    response = {
        "img_name": file_name,
        "folder_url": img_folder,
        "progress": anime_artist.progress,
        "total_steps": anime_artist.total_steps,
        "generation_complete": anime_artist.generation_complete,
        "estimated_time": anime_artist.estimated_time,
        "settings": {
            "prompt": prompt,
            "negativePrompt": negativePrompt,
            "width": width,
            "height": height,
            "num_inference_steps": num_inference_steps,
            "eta": eta,
            "guidance_scale": guidance_scale,
            "seed": seed,
            "batch_size": batch_size,
            "get_active_model": get_active_model(),
            "vae": vae_name,
        },
    }

    json_filename = "imageJson.json"
    json_filepath = os.path.join("static", json_filename)

    if not os.path.exists(json_filepath):
        with open(json_filepath, "w") as json_file:
            json.dump({file_name: response}, json_file)
    else:
        with open(json_filepath, "r") as json_file:
            existing_data = json.load(json_file)

        existing_data[file_name] = response

        with open(json_filepath, "w") as json_file:
            json.dump(existing_data, json_file)

    return jsonify(response)


@app.route("/available_models")
def available_models():
    active_model = get_active_model()

    response = {
        "all_models": print_available_models("artModel"),
        "active_models": active_model,
    }
    return jsonify(response)


@app.route("/selected_model", methods=["POST"])
def selected_model():
    selected_model = request.json["selected_model"]
    global_model_id = selected_model
    set_active_model(selected_model)
    response = {"message": "Selected model received: " + global_model_id}
    return jsonify(response)


def get_active_model():
    if os.path.exists(ACTIVE_MODEL_FILE):
        with open(ACTIVE_MODEL_FILE, "r") as file:
            active_model = file.read().strip()
            active_model = active_model.replace("--", "/")
            return active_model
    else:
        return ""

def set_active_model(model_id):
    model_id = (
        str(model_id).replace("--", "/").replace("models--", "").replace("models", "")
    )
    model_id = model_id.replace("/", "", 1)
    with open(ACTIVE_MODEL_FILE, "w") as file:
        file.write(model_id)


@app.route("/get_prompt", methods=["POST"])
def getPrompt():
    randomPrompt.prompt()


@app.route("/delete_image", methods=["POST"])
def delete_image():
    data = request.get_json()
    image_file = data.get("fileName")
    permissions = 0o755
    try:
        current_directory = os.getcwd()
        image_path = os.path.join(current_directory, "GeneratedImg", image_file)
        if os.path.exists(image_path):
            os.chmod(image_path, permissions)
            os.remove(image_path)
            return jsonify({"message": "Image deleted successfully"}), 200
        else:
            return jsonify({"error": "Image file not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.run(debug=True)
