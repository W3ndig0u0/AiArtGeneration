from flask import Flask, render_template, request, jsonify
from virtualTuber import VirtualTuber
from PIL import Image
import io

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
    generated_image = virtual_tuber.generate_art()  # Generate art using VirtualTuber
    image_data = io.BytesIO()
    generated_image.save(image_data, format='PNG')
    image_data.seek(0)
    return render_template('art.html', image_data=image_data.getvalue())

if __name__ == '__main__':
    app.run(debug=True)
