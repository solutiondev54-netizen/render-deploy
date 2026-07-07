import json
import os

CHAR_FILE = "/home/JoHn123Paul/MAAE-Core/database/characters.json"
EPI_FILE = "/home/JoHn123Paul/MAAE-Core/database/episodes.json"

def read_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def write_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def application(environ, start_response):
    path = environ.get('PATH_INFO', '')
    method = environ.get('REQUEST_METHOD', 'GET')
    
    # CORS headers for universal cross-origin mobile access
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
        ('Access-Control-Allow-Headers', 'Content-Type')
    ]
    
    if method == 'OPTIONS':
        start_response('200 OK', headers)
        return [b'']

    # Route 1: Characters
    if path == '/characters':
        start_response('200 OK', headers)
        return [json.dumps(read_json(CHAR_FILE), indent=2).encode('utf-8')]
        
    # Route 2: Episodes (Supports GET to view and POST to add)
    elif path == '/episodes':
        if method == 'POST':
            try:
                request_body_size = int(environ.get('CONTENT_LENGTH', 0))
                request_body = environ['wsgi.input'].read(request_body_size)
                new_episode_data = json.loads(request_body.decode('utf-8'))
                
                # Assign a new ID automatically
                current_episodes = read_json(EPI_FILE)
                next_id = f"EP{str(len(current_episodes) + 1).zfill(3)}"
                
                current_episodes[next_id] = new_episode_data
                write_json(EPI_FILE, current_episodes)
                
                start_response('201 Created', headers)
                return [json.dumps({"success": True, "id": next_id, "data": new_episode_data}).encode('utf-8')]
            except Exception as e:
                start_response('400 Bad Request', headers)
                return [json.dumps({"error": str(e)}).encode('utf-8')]
        
        # Default GET request handling
        start_response('200 OK', headers)
        return [json.dumps(read_json(EPI_FILE), indent=2).encode('utf-8')]
            
    # Default Root Route
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"<h1>MAAE Core Engine Operational</h1><p>Available endpoints: /characters , /episodes</p>"]
