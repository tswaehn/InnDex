from http.server import HTTPServer
import webserver.requestHandler

HOST = "localhost"
PORT = 8000
print("starting webserver {host}:{port}".format(host=HOST, port=PORT))
httpd = HTTPServer((HOST, PORT), webserver.requestHandler.MyHTTPRequestHandler)
httpd.serve_forever()
