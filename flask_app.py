import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini with the API key from Render environment variables
# Ensure your API_KEY environment variable is correctly set in Render
api_key = os.environ.get("API_KEY")
if api_key:
    genai.configure(api_key=api_key)

@app.route('/')
def index():
    # Ensure you have a templates/index.html file in your project
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()
    user_prompt = data.get('prompt', '').strip()
    
    if not api_key:
        return jsonify({"script": "System Error: API Key not configured."})
    
    if not user_prompt:
        return jsonify({"script": "Error: Please enter a plot idea."})
    
    try:
        # Change the line inside your generate() function:
model = genai.GenerativeModel('gemini-3.5-flash')
        
        prompt_text = (
            f"Write a professional, hilarious comedy script for the show 'MAAE Core'. "
            f"CAST: Mama Akos (the boss), Kofi (the troublemaker), "
            f"Papa Kofi (the mediator/absent-minded), and Akos (the sassy sister). "
            f"PLOT: {user_prompt}. "
            f"INSTRUCTIONS: Use standard script format with scene headings, "
            f"character names, and dialogue. Ensure all four characters "
            f"contribute to the comedy."
        )
        
        response = model.generate_content(prompt_text)
        return jsonify({"script": response.text})
    except Exception as e:
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
