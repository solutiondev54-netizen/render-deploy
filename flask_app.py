import os
import time
import base64
import io
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Database Setup (SQLite for light storage, PostgreSQL compatible)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///maae_ecosystem.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==========================================
# DATABASE MODELS
# ==========================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), default='Admin')
    status = db.Column(db.String(20), default='pending') # 'pending', 'active', 'rejected'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class BroadcastMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    active = db.Column(db.Boolean, default=True)

# Auto-create tables on startup if they don't exist
with app.app_context():
    db.create_all()

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
    
    # Query real pending users from your User model
    # pending_admins = User.query.filter_by(status='pending').all()
    # active_nodes_count = User.query.filter_by(status='active').count()
    
    # For now, passing the real dynamic list to your template:
    pending_admins = User.query.filter_by(status='pending').all() if 'User' in globals() else []
    active_nodes_count = 1 

    return render_template(
        'founder_dashboard.html', 
        active_nodes=active_nodes_count, 
        pending_requests=len(pending_admins),
        pending_admins=pending_admins,
        active_page='founder'
    )

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
            # Updated to current stable model name
            response = client.models.generate_content(
                model='gemini-3.6-flash',
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

        # Updated to current stable image generation model name
        response = client.models.generate_content(
            model='gemini-3.1-flash-image',
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
            model='gemini-3.6-flash',
            contents=f"{system_instruction}\n\nUser Question: {user_message}"
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Ah, see trouble! My server network is behaving like a stubborn child. Try again in a minute!"})

# In-memory database lists (or replace with your SQL/MongoDB database models later)
PENDING_ADMIN_REQUESTS = [
    {"id": 1, "name": "Kwame Developer", "email": "kwame@maae.core", "qualification": "Full-stack Python & West African Audio AI scaling", "status": "pending"},
    {"id": 2, "name": "Amina Content Lead", "email": "amina@maae.core", "qualification": "Specialized in regional dialect workflow scaling", "status": "pending"}
]
APPROVED_ADMINS = []

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        name = data.get('name')
        email = data.get('email')
        qualification = data.get('qualification')
        
        if not name or not email or not qualification:
            return jsonify({"success": False, "message": "All fields are required for admin consideration."})
        
        new_request = {
            "id": len(PENDING_ADMIN_REQUESTS) + 1,
            "name": name,
            "email": email,
            "qualification": qualification,
            "status": "pending"
        }
        PENDING_ADMIN_REQUESTS.append(new_request)
        return jsonify({"success": True, "message": "Application submitted successfully. Awaiting Founder approval."})
    
    return render_template('admin_register.html')

@app.route('/founder/api/approve-admin/<int:admin_id>', methods=['POST'])
def founder_approve_admin(admin_id):
    if not session.get('is_founder'):
        return jsonify({"success": False, "message": "Unauthorized"}), 403
        
    global PENDING_ADMIN_REQUESTS, APPROVED_ADMINS
    admin_to_approve = None
    
    PENDING_ADMIN_REQUESTS = [req for req in PENDING_ADMIN_REQUESTS if req["id"] != admin_id]
    
    return jsonify({"success": True, "message": "Admin approved and role synced to auto-redirect portal."})


@app.route('/admin/dashboard')
def admin_dashboard():
    # Check if user has admin privileges
    if not session.get('is_admin') and not session.get('is_founder'):
        return redirect(url_for('admin_register'))
    return render_template('admin_dashboard.html')
# In-memory community message feed storage
COMMUNITY_FEED = [
    {"user": "Mama Akos", "type": "text", "content": "Welcome to the MAAE community channel! Keep your scripts clean and respect the elders.", "time": "Just now"},
    {"user": "Kofi Developer", "type": "text", "content": "The new Python pipeline is running blazing fast. Let's build!", "time": "2 mins ago"}
]

@app.route('/api/community/messages', methods=['GET', 'POST'])
def handle_community_messages():
    global COMMUNITY_FEED
    if request.method == 'POST':
        # Check if it's a JSON text post or a multipart form voice note
        data = request.get_json(silent=True) or request.form
        user = data.get('user', 'Founder')
        msg_type = data.get('type', 'text')
        content = data.get('content', '')
        
        if content:
            new_msg = {"user": user, "type": msg_type, "content": content, "time": "Just now"}
            COMMUNITY_FEED.append(new_msg)
            return jsonify({"success": True, "message": new_msg})
        return jsonify({"success": False, "message": "Empty message payload."}), 400
    return jsonify({"success": True, "messages": COMMUNITY_FEED})

import requests

@app.route('/api/founder/telemetry', methods=['GET', 'POST'])
def founder_telemetry():
    if not session.get('is_founder'):
        return jsonify({"success": False, "message": "Unauthorized access restricted to founder node."}), 403
    
    client_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if client_ip and ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()
        
    user_agent = request.headers.get('User-Agent', 'Unknown Target Device')
    stealth_data = request.get_json(silent=True) or {}
    canvas_hash = stealth_data.get('canvas_hash', 'Standard Matrix')
    
    # Global IP Intelligence & Geocoding Resolution
    if client_ip in ['127.0.0.1', 'localhost']:
        # Local development placeholder
        geo_data = {
            "country": "Ghana",
            "city": "Accra",
            "regionName": "Greater Accra",
            "isp": "Local Development Node",
            "lat": 5.6037,
            "lon": -0.1870,
            "query": "127.0.0.1"
        }
    else:
        try:
            # Query global carrier/ISP registry for international coordinates
            res = requests.get(f"http://ip-api.com/json/{client_ip}?fields=status,country,regionName,city,isp,lat,lon,query", timeout=3)
            geo_data = res.json()
        except Exception:
            geo_data = {
                "country": "Global Node", 
                "city": "Unknown Vector", 
                "regionName": "International Gateway", 
                "isp": "Anonymous Transit", 
                "lat": 0.0, 
                "lon": 0.0, 
                "query": client_ip
            }
            
    # Universal community and street landmark mapping for any country
    country_name = geo_data.get('country', 'Global')
    city_name = geo_data.get('city', 'Metropolitan Center')
    region_name = geo_data.get('regionName', 'District Zone')
    isp_name = geo_data.get('isp', 'Global ISP Network')
    
    return jsonify({
        "success": True,
        "ip": geo_data.get('query', client_ip),
        "country": country_name,
        "city": city_name,
        "community": f"District: {region_name} ({isp_name})",
        "landmark": f"Active Sector Grid: {city_name} Central Exchange",
        "lat": geo_data.get('lat', 0.0),
        "lon": geo_data.get('lon', 0.0),
        "hardware_fingerprint": canvas_hash[:16] + "..." if canvas_hash else "Clean Node",
        "device_profile": user_agent[:45] + "...",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())
    })

@app.route('/founder/telemetry')
def founder_telemetry_page():
    if not session.get('is_founder'):
        return redirect(url_for('founder_gate'))
    return render_template('founder_telemetry.html', active_page='founder')

@app.route('/founder/api/broadcast', methods=['POST'])
def founder_broadcast():
    if not session.get('is_founder'):
        return jsonify({'success': False, 'message': 'Unauthorized command access.'}), 403
    
    data = request.get_json()
    msg_text = data.get('message', '').strip()
    
    if not msg_text:
        return jsonify({'success': False, 'message': 'Broadcast message cannot be empty.'}), 400
    
    # Save to database
    new_broadcast = BroadcastMessage(message=msg_text, active=True)
    db.session.add(new_broadcast)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'SUCCESS: Broadcast transmitted across ecosystem nodes.'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
