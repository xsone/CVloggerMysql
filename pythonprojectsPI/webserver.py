from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import json

hostName = '192.168.178.144'
serverPort = 8000

elecACTverbruik = 111
elecACTgeleverd = 222


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
        #self.wfile.write(bytes('#', "utf-8"))
        self.wfile.write(bytes(str(elecACTverbruik) + str(elecACTgeleverd), "utf-8"))
        #self.wfile.write(bytes(';', "utf-8"))
        #self.wfile.write(bytes(str(elecACTgeleverd), "utf-8"))
        #self.wfile.write(bytes(';', "utf-8"))



        #self._set_headers()
        #self.wfile.write(json.dumps({'hello': 'world', 'received': 'ok'}))

if __name__ == "__main__":
    # webServer = HTTPServer((hostName, serverPort), MyServer)
    # print("Server started http://%s:%s" % (hostName, serverPort))
    webServer = HTTPServer(("", serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))
    
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")