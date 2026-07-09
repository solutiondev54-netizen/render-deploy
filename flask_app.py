import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

import random

@app.route('/generate', methods=['POST'])
def generate():
    # This is your list of different story options
    story_options = [
        "EPISODE: EP002 - The Jollof Thief\n\nMama Akos enters the kitchen and finds the pot completely empty. She screams!",
        "EPISODE: EP003 - The Midnight Masquerade\n\nThe wooden mask on the wall starts whispering secrets in the middle of the night.",
        "EPISODE: EP004 - Market Day Mayhem\n\nKofi tries to sell a fabric that isn't actually his. The market queen is not happy."
    ]
    
    # This picks one story randomly every time you click the button
    chosen_script = random.choice(story_options)
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
