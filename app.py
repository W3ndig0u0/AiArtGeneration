from flask import Flask, render_template, request, jsonify
from virtualTuber import VirtualTuber
from artGeneration import AnimeArtist
from fileSize import print_available_models, get_folder_size, convert_size
from loadModel import load_model
from accelerate import Accelerator
from diffusers import DiffusionPipeline

app = Flask(__name__)
virtual_tuber = VirtualTuber()
anime_artist = AnimeArtist()

@app.route('/process_input', methods=['POST'])
def process_input():
    user_input = request.json['user_input']
    response = virtual_tuber.run(user_input)
    return jsonify({'response': response})

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/art')
def art():
    return render_template('art.html')

@app.route('/generate_art', methods=['POST'])
def generate_art():
    prompt = request.json['prompt']
    num_inference_steps = int(request.json['num_inference_steps'])
    eta = float(request.json['eta'])
    guidance_scale = int(request.json['guidance_scale'])

    save_folder = "./GeneratedImg"  # Define the save_folder variable here
    initial_generation = request.json.get('initial_generation', False)

    # accelerator = Accelerator()
    generator = DiffusionPipeline.from_pretrained("stablediffusionapi/anime-model-v2")
    anime_artist.generator = generator
    intermediate_folder, final_save_path = anime_artist.generate_art(prompt, 512, 512, num_inference_steps, eta, guidance_scale, save_folder, initial_generation)

    intermediate_url = f"/{intermediate_folder}/"
    final_url = f"/{final_save_path}" 

    response = {
        'intermediate_url': intermediate_url,
        'final_url': final_url,
        'progress': anime_artist.progress,
        'total_steps': anime_artist.total_steps,
        'generation_complete': anime_artist.generation_complete,
        'estimated_time': anime_artist.estimated_time
    }

    return jsonify(response)






if __name__ == '__main__':
    app.run(debug=True)
