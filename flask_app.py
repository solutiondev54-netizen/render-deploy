import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini with the API key from Render environment variables
genai.configure(api_key=os.environ.get("API_KEY"))

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
        # Change this line:
        model = genai.GenerativeModel('gemini-1.5-flash-002')
        prompt_text = (
            f"Write a professional, hilarious comedy script for the show 'MAAE Core'. "
            f"CAST: Mama Akos (the boss), Kofi (the troublemaker), Papa Kofi (the mediator/absent-minded), and Akos (the sassy sister). "
            f"PLOT: {user_prompt}. "
            f"INSTRUCTIONS: Use standard script format with scene headings, character names, and dialogue. Ensure all four characters contribute to the comedy."
        )
        response = model.generate_content(prompt_text)
        return jsonify({"script": response.text})
    except Exception as e:
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

@app.route('/render-video', methods=['POST'])
def render_video():
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
