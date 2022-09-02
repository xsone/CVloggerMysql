#### Werkt!!
# import http.server
# import socketserver
#
# #hostName = "localhost"  #PC is 192.168.178.109
# from http import client
#
# import requests
#
# serverPort = 8000
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# #with socketserver.TCPServer((hostName, serverPort), Handler) as httpd:
# with socketserver.TCPServer(("", serverPort), Handler) as httpd:
#     print("Serving At Localhost PORT", serverPort)
#     httpd.serve_forever()
###Werkt!!

#If you are using Python 3.x, you should replace your import statement by: from http.server import BaseHTTPRequestHandler, HTTPServer
# from http.server import BaseHTTPRequestHandler, HTTPServer
# import socketserver
# import json
# import cgi
#
#
# class Server(BaseHTTPRequestHandler):
#     def _set_headers(self):
#         self.send_response(200)
#         self.send_header('Content-type', 'application/json')
#         self.end_headers()
#
#     def do_HEAD(self):
#         self._set_headers()
#
#     # GET sends back a Hello world message
#     def do_GET(self):
#         self._set_headers()
#         self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))
#
#     # POST echoes the message adding a JSON field
#     def do_POST(self):
#         ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
#
#         # refuse to receive non-json content
#         if ctype != 'application/json':
#             self.send_response(400)
#             self.end_headers()
#             return
#
#         # read the message and convert it into a python dictionary
#         length = int(self.headers.getheader('content-length'))
#         message = json.loads(self.rfile.read(length))
#
#         # add a property to the object, just to mess with data
#         message['received'] = 'ok'
#
#         # send the message back
#         self._set_headers()
#         self.wfile.write(json.dumps(message))
#
#
# def run(server_class=HTTPServer, handler_class=Server, port=8000):
#     server_address = ('', port)
#     httpd = server_class(server_address, handler_class)
#
#     print('Starting httpd on port %d...',  port)
#     httpd.serve_forever()
#
#
# if __name__ == "__main__":
#     from sys import argv
#
#     if len(argv) == 2:
#         run(port=int(argv[1]))
#     else:
#         run()


# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = '192.168.178.109'
serverPort = 8000

ElecActueelVerbruikt = 111
ElecActueelGeleverd = 222




class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        #self.send_header("Content-type", "text/html")
        #self.end_headers()
        # self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title></head>", "utf-8"))
        # self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        # self.wfile.write(bytes("<body>", "utf-8"))
        # self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
        # self.wfile.write(bytes("</body></html>", "utf-8"))
        #self.send_header("Content-type", "application/json")
        self.wfile.write(bytes('#', "utf-8"))
        self.wfile.write(bytes(str(ElecActueelVerbruikt), "utf-8"))
        self.wfile.write(bytes(';', "utf-8"))
        self.wfile.write(bytes(str(ElecActueelGeleverd), "utf-8"))
        self.wfile.write(bytes(';', "utf-8"))



        #self._set_headers()
        #self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))

if __name__ == "__main__":
    # webServer = HTTPServer((hostName, serverPort), MyServer)
    # print("Server started http://%s:%s" % (hostName, serverPort))
    webServer = HTTPServer(("", serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    ElecActueelVerbruikt = ElecActueelVerbruikt + 1
    ElecActueelGeleverd = ElecActueelGeleverd + 1
    if (ElecActueelVerbruikt > 999): ElecActueelVerbruikt = 0
    if (ElecActueelGeleverd > 999): ElecActueelGeleverd = 0

    try:
        webServer.serve_forever()



    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")