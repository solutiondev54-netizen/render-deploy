import os
import time
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
import gc

# Enable garbage collection to keep container memory clean
gc.enable()

app = Flask(__name__)
CORS(app)

# Initialize the official Google GenAI client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    
    if not user_prompt:
        return jsonify({
            'status': 'error',
            'message': 'Please enter a plot idea or select a character preset.'
        }), 400

    # Structured prompt template to lock in character dynamics and behaviors
    structured_content = (
        "You are the master comedy scriptwriter for MAAE CORE, a high-end African production suite. "
        f"Generate a hilarious, highly relatable West African comedy sketch script based on this idea: {user_prompt}. "
        "STRICT FAMILY CHARACTER RULES & BEHAVIORS: "
        "- AKOS: The witty, dramatic daughter/sister. Always stressed, talks fast, defends her wardrobe or dignity fiercely. "
        "- KOFI: Akos's brother. Cheeky, annoying, loves pulling pranks and eating food that isn't his. "
        "- WAMA AKOS: The mother. Dramatic, uses epic African mother psychological warfare and religious quotes. "
        "- PAPA KOFI / PAPA AKOS: The father. Old-school, strict authority, easily distracted by food or football. "
        "Format cleanly with **SCENE START**, **SETTING**, character names in bold caps, action tags in parentheses, and dialogue."
    )

    max_retries = 3
    base_delay = 4

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-3-flash-preview',
                contents=structured_content
            )
            
            if response and response.text:
                return jsonify({'status': 'success', 'script': response.text}), 200
            else:
                raise ValueError("Received an empty response payload from the model.")

        except Exception as e:
            error_message = str(e)
            print(f"GENERATION WARNING [Attempt {attempt + 1}/{max_retries}]: {error_message}")
            
            if attempt < max_retries - 1:
                sleep_duration = base_delay * (2 ** attempt)
                time.sleep(sleep_duration)
            else:
                return jsonify({
                    'status': 'error',
                    'script': f"SERVER ERROR: Model capacity exhausted or rate limit reached. Details: {error_message}"
                }, 500)

# --- Video Rendering Placeholder Route ---
@app.route('/api/render-video', methods=['POST'])
def render_video():
    # Kept lightweight with no local disk usage to prevent server bloat
    return jsonify({
        'status': 'success',
        'video_url': 'https://example.com/placeholder_video.mp4'
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
