import threading
import webview
from app import app  # Imports your existing Flask app instance

def start_server():
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window(
        'MAAE Core | Production Studio Suite', 
        'http://127.0.0.1:5000', 
        width=1200, 
        height=800,
        min_size=(800, 600)
    )
    webview.start()
