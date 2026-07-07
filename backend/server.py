import http.server
import json
import os

PORT = 9090
DB_FILE = "database/characters.json"

class MAAECoreHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.wfile.write(json.dumps(data, indent=2).encode("utf-8"))
        else:
            self.wfile.write(json.dumps({"error": "Database file not found"}).encode("utf-8"))

print(f"📡 MAAE Core Micro-API engine is booting up on port {PORT}...")
server = http.server.HTTPServer(("0.0.0.0", PORT), MAAECoreHandler)
server.serve_forever()
