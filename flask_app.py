import os
import random
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', 'No prompt provided')
    
    # Process the prompt
    response_text = f"Feature film based on: {user_prompt}. (System: Story logic processing...)"
    return jsonify({"script": response_text})

@app.route('/render-video', methods=['POST'])
def render_video():
    # Currently pointing to demo video
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
