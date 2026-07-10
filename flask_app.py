import os
from flask import Flask, request, jsonify
from google import genai

app = Flask(__name__)

# Initialize the client with your API key from environment variables
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# This route must match the fetch() URL in your frontend JavaScript
@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.json
    user_prompt = data.get('prompt', '')

    try:
        # Using Flash model for memory stability on free tier
        response = client.models.generate_content(
            model='models/gemini-3.5-flash',
            contents=f"Write a comedy script for 'MAAE Core'. PLOT: {user_prompt}."
        )
        return jsonify({"script": response.text})
    except Exception as e:
        # Returning a 500 status with error details
        return jsonify({"script": f"AI Engine Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
