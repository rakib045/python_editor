import http.server
import socketserver
import webbrowser

server = '127.0.0.1'
port = '8000'

if __name__ == "__main__":
    handler_object = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", int(port)), handler_object) as httpd:
        print("Serving web-server at : http://localhost:" + port)
        webbrowser.open("http://localhost:" + port )
        httpd.serve_forever()