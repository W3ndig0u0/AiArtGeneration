from flask import Flask, render_template, request, jsonify
from virtualTuber import VirtualTuber

app = Flask(__name__)
virtual_tuber = VirtualTuber()

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

@app.route('/get_generated_art')
def get_generated_art():
    generated_art_url = virtual_tuber.get_generated_art_url()  # Modify this method in the VirtualTuber class to return the URL of the generated art
    return jsonify({'generated_art_url': generated_art_url})

if __name__ == '__main__':
    app.run(debug=True)
