import http.server
import socketserver
import webbrowser
import os
import sys
from generate_site import build

PORT = 4000
DIRECTORY = "_site"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def main():
    print("Building site...")
    build()
    
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"\n==========================================")
        print(f" Site preview running at: {url}")
        print(f" Press Ctrl+C to stop the server")
        print(f"==========================================\n")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == '__main__':
    main()
