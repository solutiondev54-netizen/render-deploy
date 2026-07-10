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
    user_prompt = data.get('prompt', '').strip()
    
    # Requirement: Ensure the prompt is not empty
    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot or idea to generate a script."})
    
    # Generate full script structure
    full_script = f"""
    TITLE: {user_prompt.upper()}
    
    [SCENE START]
    EXT. STUDIO LOCATION - DAY
    
    The scene opens with the energy of the prompt: {user_prompt}.
    
    CHARACTER A: We have to get this right this time.
    
    CHARACTER B: (Looking at the camera) The script says it's going to be legendary.
    
    [SCENE END]
    """
    
    return jsonify({"script": full_script})

@app.route('/render-video', methods=['POST'])
def render_video():
    # Currently pointing to demo video
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
