from flask import Flask, render_template, request, jsonify, send_from_directory
from artGeneration import AnimeArtist
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
import os
import json

app = Flask(__name__, static_url_path="/static", static_folder="static")
anime_artist = AnimeArtist()


@app.route("/GeneratedImg/<path:path>")
def send_img(path):
    return send_from_directory("GeneratedImg", path)


@app.route("/process_input", methods=["POST"])
def process_input():
    user_input = request.json["user_input"]
    response = virtual_tuber.run(user_input)
    return jsonify({"response": response})


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/art")
def art():
    return render_template("art.html")


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
    save_folder = "GeneratedImg"

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


if __name__ == "__main__":
    app.run(debug=True)
