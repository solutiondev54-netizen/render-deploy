import os
import time 
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
import gc
# ... after your imports
gc.enable()

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()

    if not user_prompt:
        return jsonify({'status': 'error', 'message': 'Please enter a plot idea.'})

    # Retry logic with backoff
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Write a professional, witty comedy script about: {user_prompt}"
            )
            return jsonify({'script': response.text})
           
        # Retry logic with backoff
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Write a professional, witty comedy script about: {user_prompt}"
            )
            return jsonify({'script': response.text})
        except Exception as e:
            print(f"GENERATION ERROR: {str(e)}")
            if attempt < 2:
                time.sleep(3)
                continue
            else:
                return jsonify({'script': "System Is Busy: kindly try again in a few seconds."}), 503

# --- Video R---
@app.route('/api/render-video', methods=['POST'])
def render_video():
    # Keep this logic simple to avoid memory spikes
    return jsonify({'status': 'success', 'video_url': 'https://example.com/placeholder_video.mp4'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
