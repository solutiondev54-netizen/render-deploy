import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from google import genai
from google.genai import types

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
        return jsonify({"script": "Error: Please enter a plot idea."})

    system_instruction = "You are the 'MAAE Core' Script Engine. Write professional, witty comedy scripts. AUTHORIZED CAST ONLY: Kafi, Mama Akos, Papa Kafi, Akos Kafi's sister."

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=f"{system_instruction}\n\nPLOT: {user_prompt}"
        )
        return jsonify({"script": response.text})
    except Exception as e:
        return jsonify({"script": f"AI Engine Error: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
