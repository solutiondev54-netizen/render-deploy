import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# Initialize the client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    client = None
else:
    client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    if client is None:
        return jsonify({"script": "Error: AI Client not initialized."})
    
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    
    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot idea."})
    
    try:
        # SYSTEM DIRECTIVE: Strict Character Enforcement
        prompt = f"""
        You are the 'MAAE Core' Script Engine. 
        Your task is to write professional, witty comedy scripts.

        AUTHORIZED CAST ONLY:
        - Kofi
        - Mama Akos
        - Papa Kofi
        - Akos Kofi's sister

        STRICT RULES:
        1. IF a user prompt mentions a character NOT in the 'AUTHORIZED CAST', you MUST ignore that character. 
        2. DO NOT create background characters or extras (like 'Chidi'). 
        3. Keep the interaction between the authorized characters only.
        4. If the prompt implies a conflict, resolve it using only the characters listed above.
        
        PLOT: {user_prompt}
        """
        
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=prompt
        )
        return jsonify({"script": response.text})
        return jsonify({"script": response.text})
    except Exception as e:
        # Indented exactly 8 spaces to be inside the 'except' block
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

# You will need to install: google-cloud-aiplatform
from google.cloud import aiplatform

@app.route('/api/render-video', methods=['POST'])
def render_video():
    data = request.json
    script = data.get('script')
    
    # Vertex AI initialization
    aiplatform.init(project='your-project-id', location='us-central1')
    
    # We call the model directly
    # This keeps everything in the Google AI ecosystem
    video_response = aiplatform.Model('veo-model-id').predict(instances=[{"prompt": script}])
    
    return jsonify({"status": "success", "video_url": video_response.url})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
