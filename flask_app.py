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
    stories = [
        "EP002 - Jollof Retaliation: Mama Akos finds the pot empty!",
        "EP003 - The Mask's Revenge: The wooden mask on the wall starts whispering.",
        "EP004 - Market Mayhem: Kofi gets caught in a fabric deal gone wrong."
    ]
    chosen_script = random.choice(stories)
    return jsonify({"script": chosen_script})

@app.route('/render-video', methods=['POST'])
def render_video():
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
