import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Initialize the client
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()

    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot idea."})

    system_instruction = """
    You are the 'MAAE Core' Script Engine. Your task is to write professional, witty comedy scripts.
    AUTHORIZED CAST ONLY: Kafi, Mama Akos, Papa Kafi, Akos Kafi's sister.
    STRICT RULES:
    1. If a user prompt mentions a character NOT in the 'AUTHORIZED CAST', ignore that character.
    2. Do not create background characters or extras.
    3. Keep the interaction between authorized characters only.
    """

    try:
        # Using gemini-3.5-flash (Free Tier)
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"{system_instruction}\n\nPLOT: {user_prompt}"
        )
        return jsonify({"script": response.text})
    except Exception as e:
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

import os


from google import genai
from google.genai import types

@app.route('/api/render-video', methods=['POST'])
def render_video():
    data = request.get_json()
    script = data.get('script')
    
    try:
        # Initialize client with your existing key
        client = genai.Client() 
        
        # Use the correct method for video generation
        # 'veo-3.1-fast-generate-preview' is the supported model ID for AI Studio
        response = client.models.generate_videos(
            model="veo-3.1-fast-generate-preview",
            prompt=script,
            config=types.GenerateVideosConfig()
        )
        
        return jsonify({
            "status": "success",
            "video_url": "Video generation initiated" # Adjust based on how you want to handle the response
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
        
# ... (all your existing routes here) ...

# CRITICAL: Gunicorn needs this to find the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
