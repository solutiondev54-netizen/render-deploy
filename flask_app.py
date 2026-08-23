import os
import time
import base64
import io
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
from google import genai
from google.genai import types
import gc

# Enable garbage collection to keep container memory clean
gc.enable()

app = Flask(__name__)
CORS(app)

# Secure Session Secret Key
app.secret_key = os.environ.get("SECRET_KEY", "maae-ecosystem-supreme-key-2026")

# Initialize the official Google GenAI client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# Set your secret Founder Passcode/PIN here (or configure via environment variable)
FOUNDER_PASSCODE = os.environ.get("FOUNDER_PASSCODE", "MAAE-FOUNDER-2026-SECURE")


# ==========================================
# CORE VIEW & FOUNDER NAVIGATION ROUTES
# ==========================================

@app.route('/')
def studio():
    return render_template('studio.html', active_page='studio')

@app.route('/vault')
def vault():
    return render_template('vault.html', active_page='vault')

@app.route('/community')
def community():
    return render_template('community.html', active_page='community')

@app.route('/founder')
def founder():
    return render_template('founder.html', active_page='founder')


# ==========================================
# SECURE FOUNDER COMMAND & GATEWAY ROUTES
# ==========================================

@app.route('/founder/gate', methods=['GET', 'POST'])
def founder_gate():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        entered_pass = data.get('passcode')
        if entered_pass == FOUNDER_PASSCODE:
            session['is_founder'] = True
            return jsonify({"success": True, "redirect": url_for('founder_dashboard')})
        else:
            return jsonify({"success": False, "message": "Invalid Founder Security Key"})
    return render_template('founder_gate.html')

@app.route('/founder/dashboard')
def founder_dashboard():
    if not session.get('is_founder'):
        return redirect(url_for('founder_gate'))
    return render_template('founder_dashboard.html', active_page='founder')

@app.route('/founder/logout')
def founder_logout():
    session.pop('is_founder', None)
    return redirect(url_for('founder_gate'))


# ==========================================
# API MATRIX & AI GENERATION ENDPOINTS
# ==========================================

@app.route('/api/generate', methods=["POST"])
def generate():
    data = request.get_json() or {}
    user_prompt = data.get('prompt', '').strip()

    if not user_prompt:
        return jsonify({
            'status': 'error',
            'message': 'Please enter a plot idea or select a character preset.'
        }), 400

    # Structured prompt template to lock in character dynamics and behaviors
    structured_content = (
        "You are the master comedy scriptwriter for MAAE CORE, a high-end African production suite. "
        f"Generate a hilarious, highly relatable West African comedy sketch script based on this idea: {user_prompt}. "
        "STRICT FAMILY CHARACTER RULES & BEHAVIORS: "
        "- AKOS: The witty, dramatic daughter/sister. Always stressed, talks fast, defends her wardrobe or dignity fiercely. "
        "- KOFI: Akos's brother. Cheeky, annoying, loves pulling pranks and eating food that isn't his. "
        "- MAMA AKOS: The mother. Dramatic, uses epic African mother psychological warfare and religious quotes. "
        "- PAPA KOFI / PAPA AKOS: The father. Old-school, strict authority, easily distracted by food or football. "
        "Format cleanly with **SCENE START**, **SETTING**, character names in bold caps, action tags in parentheses, and dialogue."
    )

    max_retries = 3
    base_delay = 4

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=structured_content
            )

            if response and response.text:
                return jsonify({'status': 'success', 'script': response.text}), 200
            else:
                raise ValueError("Received an empty response payload from the model.")

        except Exception as e:
            error_message = str(e)
            print(f"GENERATION WARNING [Attempt {attempt + 1}/{max_retries}]: {error_message}")

            if attempt < max_retries - 1:
                sleep_duration = base_delay * (2 ** attempt)
                time.sleep(sleep_duration)
            else:
                return jsonify({
                    'status': 'error',
                    'script': f'SERVER ERROR: Model capacity exhausted or rate limit reached. Details: {error_message}'
                }, 500)

@app.route('/api/render-video', methods=['POST'])
def render_video():
    try:
        data = request.get_json() or {}
        user_prompt = data.get('prompt', '')

        cultural_guardrail = "authentic West African subject, rich natural melanin skin tones, African heritage, natural lighting"
        realism_enhancers = "shot on 35mm lens, Fujifilm Eterna film stock, anamorphic lighting, professional color grading"

        if user_prompt:
            final_prompt = f"{user_prompt}, featuring {cultural_guardrail}, {realism_enhancers}"
        else:
            final_prompt = f"Cinematic professional portrait of a {cultural_guardrail}, {realism_enhancers}"

        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=final_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
            ),
        )

        image_base64 = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_bytes = part.inline_data.data
                image_base64 = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
                break

        if image_base64:
            return jsonify({
                'status': 'success',
                'url': image_base64
            })
        else:
            return jsonify({
                'status': 'success',
                'url': 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=1200&q=80'
            })

    except Exception as e:
        print(f"Visual Generation Error: {str(e)}")
        return jsonify({
            'status': 'success',
            'url': 'https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?auto=format&fit=crop&w=1200&q=80'
        })

@app.route('/api/mama-akos-chat', methods=['POST'])
def mama_akos_chat():
    data = request.get_json() or {}
    user_message = data.get('message', '')

    system_instruction = (
        "You are 'Mama Akos', a funny, street-smart, loving, and dramatic African mother "
        "who acts as the virtual guide for this MAAE Core script production and audio studio app. "
        "Your job is to answer user questions about how to use the app (generating scripts, clicking name tags, "
        "choosing dialects, rendering videos, and using text-to-speech audio). "
        "Always respond in a warm, witty, humorous African mother lifestyle tone—use relatable "
        "expressions, loving scoldings, and simple layman terms. Keep it punchy, engaging, and very helpful."
    )

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=f"{system_instruction}\n\nUser Question: {user_message}"
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Ah, see trouble! My server network is behaving like a stubborn child. Try again in a minute!"})


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
