from flask import Flask, render_template, request, jsonify, send_from_directory
from artGeneration import AnimeArtist
from virtualTuber import VirtualTuber
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from fileSize import print_available_models
import os
import json


app = Flask(__name__, static_url_path="/static", static_folder="static")
anime_artist = AnimeArtist()
virtualTuber = VirtualTuber()
image_folder = "GeneratedImg"
ACTIVE_MODEL_FILE = "active_model.txt"
# model_id = "andite/pastel-mix"


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.json["user_input"]
    response = virtualTuber.run(user_input)
    return jsonify({"response": response})


@app.route("/")
def home():
    virtualTuber.call()
    return render_template("index.html")


@app.route("/art")
def art():
    return render_template("art.html")


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
    negativePromt = request.json["negativePromt"]
    num_inference_steps = int(request.json["num_inference_steps"])
    eta = float(request.json["eta"])
    guidance_scale = int(request.json["guidance_scale"])
    width = int(request.json.get("width", 512))
    height = int(request.json.get("height", 512))
    batch_size = int(request.json.get("batch_size", 1))
    seed = int(request.json.get("seed", -1))

    initial_generation = request.json.get("initial_generation", False)
    save_folder = "GeneratedImg/"

    print(get_active_model())

    img_folder, file_name = anime_artist.generate_art(
        prompt,
        width,
        height,
        num_inference_steps,
        eta,
        negativePromt,
        guidance_scale,
        save_folder,
        seed,
        batch_size,
        get_active_model(),
        initial_generation,
    )

    img_folder = f"{img_folder}/"
    file_name = f"{file_name}.png"

    response = {
        "folder_url": img_folder,
        "img_name": file_name,
        "progress": anime_artist.progress,
        "total_steps": anime_artist.total_steps,
        "generation_complete": anime_artist.generation_complete,
        "estimated_time": anime_artist.estimated_time,
    }

    print(response)
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
        
def remove_first_word_before_slash(string):
    if '/' in string:
        return string.split('/', 1)[1]
    else:
        return string
def set_active_model(model_id):
    model_id = str(model_id).replace("--", "/").replace("models--", "").replace("models", "")
    model_id = model_id.replace('/', '', 1)  # Remove the first '/'
    with open(ACTIVE_MODEL_FILE, "w") as file:
        file.write(model_id)


if __name__ == "__main__":
    app.run(Debug=True)
