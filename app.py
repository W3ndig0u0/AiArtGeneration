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

if __name__ == '__main__':
    app.run(debug=True)