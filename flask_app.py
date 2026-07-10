import os
import logging
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize the Gemini Client
# The SDK automatically uses GEMINI_API_KEY from environment variables
try:
    client = genai.Client()
except Exception as e:
    logger.error(f"Failed to initialize Gemini Client: {e}")

# --- Routes ---

@app.route('/')
def index():
    """Serves the main frontend page."""
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple route to verify the server is running."""
    return jsonify({"status": "healthy", "message": "Script Engine is online"})

@app.route('/api/generate', methods=['POST'])
def generate():
    """Handles the script generation request."""
    data = request.get_json()
    
    if not data or 'prompt' not in data:
        return jsonify({"error": "No prompt provided"}), 400
        
    user_prompt = data.get('prompt', '').strip()
    if not user_prompt:
        return jsonify({"error": "Prompt cannot be empty"}), 400
    
    try:
        logger.info(f"Generating script for: {user_prompt[:50]}...")
        
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=(
                f"Write a professional, hilarious comedy script for the show 'MAAE Core'. "
                f"CAST: Mama Akos, Kofi, Papa Kofi, and Akos. "
                f"PLOT: {user_prompt}. "
                f"INSTRUCTIONS: Use standard script format."
            )
        )
        return jsonify({"script": response.text})
        
    except Exception as e:
        logger.error(f"Generation Error: {e}")
        return jsonify({"error": f"AI Engine failed: {str(e)}"}), 500

@app.route('/api/video', methods=['POST'])
def render_video():
    """Endpoint for future video rendering logic."""
    return jsonify({"status": "success", "video_url": "https://vjs.zencdn.net/v/oceans.mp4"})

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render, default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
