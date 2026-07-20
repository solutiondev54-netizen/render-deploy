import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types
from google.cloud import storage 

app = Flask(__name__)
CORS(app)

# Initialize the client
api_key = os.environ.get("GEMINI_API_KEY")
# Added retry options to handle "busy" (429) errors gracefully
retry_policy = types.HttpRetryOptions(initial_delay=1.0, attempts=5, http_status_codes=[429, 500, 503])
client = genai.Client(api_key=api_key, http_options=types.HttpOptions(retry_options=retry_policy))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()

    if not user_prompt:
        return jsonify({'status': 'error', 'message': 'Please enter a plot idea.'})

    system_instruction = "You are the MAAE Core Script Engine. Write professional, witty comedy scripts."

    try:
        # Use a more lightweight call
        response = client.models.generate_content(
            model='gemini-1.5-flash',
            contents=f"{system_instruction}\n\nPLOT: {user_prompt}"
        )
        
        # Explicitly extract text and return immediately
        script_text = response.text
        return jsonify({'script': script_text})

    except Exception as e:
        # Catch the error and return JSON so the frontend doesn't show the '<' error
        return jsonify({'script': f"Engine Error: {str(e)}"}), 500

# --- Video Rendering Route ---
@app.route('/api/render-video', methods=['POST'])
def render_video():
    data = request.get_json()
    script_text = data.get('script', '')

    if not script_text:
        return jsonify({'status': 'error', 'message': 'No script provided'})

    # This is where your video rendering logic goes.
    # For now, this returns a success message to test your button connection.
    return jsonify({
        'status': 'success', 
        'video_url': 'https://example.com/placeholder_video.mp4' 
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
