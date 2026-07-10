import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

# DEBUG: Print environment variables to logs (This will help us see if Render is loading your key)
print(f"DEBUG: GEMINI_API_KEY loaded: {'YES' if os.environ.get('GEMINI_API_KEY') else 'NO'}", file=sys.stderr)

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    # This will show up in your Render Logs exactly what is wrong
    print("CRITICAL ERROR: GEMINI_API_KEY not found in environment!", file=sys.stderr)
    client = None
else:
    client = genai.Client(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if client is None:
        return jsonify({"script": "Error: AI Client not initialized. Check your API key in Render settings."})
    
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    
    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot idea."})
    
    try:
        # We use the most generic, widely supported model name
        response = client.models.generate_content(
            model='models/gemini-3.5-flash'
            contents=f"Write a comedy script for 'MAAE Core'. PLOT: {user_prompt}."
        )
        return jsonify({"script": response.text})
    except Exception as e:
        # This will tell us the exact Google API error in your browser
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
