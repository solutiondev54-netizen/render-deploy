import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    local_script = (
        "### EPISODE: EP002 - Jollof Retaliation\n\n"
        "### SCENE 1\n\n"
        "**INT. AKOS'S LIVING ROOM - DAY**\n\n"
        "A vibrant Ghanaian living room clashing gloriously with Ankara print fabrics. "
        "A large wooden mask hangs on the wall.\n\n"
        "**MAMA AKOS** (60s, a complete force of nature) paces wildly like a caged lioness. "
        "She stops and shakes her fist at the mask.\n\n"
        "**MAMA AKOS**\n"
        "> Mask! Do you see this humiliation?! Stolen! My masterpiece jollof... gone! "
        "I put precisely seven scotch bonnet peppers for the true Ghanaian kick! "
        "This is a culinary vendetta! You will tell me who did this, or I swear I will replace you with a picture of Beyoncé!\n\n"
        "*She spins on her heel and marches into the kitchen, muttering about culinary traitors.*"
    )
    return jsonify({"script": local_script})

@app.route('/render-video', methods=['POST'])
def render_video():
    # Using an open-access video stream from VideoJS that allows direct web embedding
    return jsonify({
        "status": "success",
        "video_url": "https://vjs.zencdn.net/v/oceans.mp4"
    })

if __name__ == '__main__':
    app.run(debug=True)
