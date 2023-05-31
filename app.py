from flask import Flask, render_template, request, jsonify
from virtualTuber import VirtualTuber


app = Flask(__name__)
virtual_tuber = VirtualTuber()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    response = virtual_tuber.generate_response(user_input)
    return jsonify({'response': response})


if __name__ == '__main__':
    print("Using device:", virtual_tuber.device)
    app.run()
