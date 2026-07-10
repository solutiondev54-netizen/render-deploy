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
        # Indented exactly 8 spaces to be inside the 'try' block
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=f"Write a comedy script for 'MAAE Core'. PLOT: {user_prompt}."
        )
        return jsonify({"script": response.text})
    except Exception as e:
        # Indented exactly 8 spaces to be inside the 'except' block
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
