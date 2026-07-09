import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

import random

import random

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # A library of different stories
    stories = [
        "EPISODE: EP002 - Jollof Retaliation\nMama Akos finds the pot empty!",
        "EPISODE: EP003 - The Mask's Revenge\nThe wooden mask on the wall starts whispering.",
        "EPISODE: EP004 - Market Mayhem\nKofi gets caught in a fabric deal gone wrong."
    ]
    
    # This picks one random story every time the button is clicked
    chosen_script = random.choice(stories)
    return jsonify({"script": chosen_script})

@app.route('/render-video', methods=['POST'])
def render_video():
    # Using an open-access video stream from VideoJS that allows direct web embedding
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
