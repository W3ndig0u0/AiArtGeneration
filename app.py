from flask import Flask, render_template, request, jsonify
from virtualTuber import VirtualTuber
from artGeneration import AnimeArtist

app = Flask(__name__)
virtual_tuber = VirtualTuber()
animeArtist = AnimeArtist()

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

    animeArtist.generate_art(prompt, num_inference_steps, eta, guidance_scale)  # Modify this method in the AnimeArtist class

    return jsonify({'message': 'Art generation started'})

if __name__ == '__main__':
    app.run(debug=True)
