import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini with the API key from Render environment variables
api_key = os.environ.get("API_KEY")
genai.configure(api_key=api_key)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    
    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot idea."})
    
    try:
        # We are using the standard model identifier
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt_text = (
            f"Write a professional, hilarious comedy script for the show 'MAAE Core'. "
            f"CAST: Mama Akos, Kofi, Papa Kofi, and Akos. "
            f"PLOT: {user_prompt}. "
            f"INSTRUCTIONS: Use standard script format."
        )
        response = model.generate_content(prompt_text)
        return jsonify({"script": response.text})
    except Exception as e:
        # This will return the exact API error to your browser
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
