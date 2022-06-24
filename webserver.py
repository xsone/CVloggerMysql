#### Werkt!!
import http.server
import socketserver

hostName = "localhost"  #PC is 192.168.178.109
serverPort = 8080

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer((hostName, serverPort), Handler) as httpd:
    print("Serving At Localhost PORT", serverPort)
    httpd.serve_forever()
###Werkt!!

# # Python 3 server example
#
import time
# hostName = "localhost"  #PC is 192.168.178.109
# serverPort = 88
# #
# class webServer(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-type", "text/html")
#         self.end_headers()
#         self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
#         self.wfile.write(bytes("<body>", "utf-8"))
#         self.wfile.write(bytes("<p>This is an example web server.</p>", "utf-8"))
#         self.wfile.write(bytes("</body></html>", "utf-8"))
#
# if __name__ == "__main__":
#     webServer = TCPServer((hostName, serverPort), webServer)
#     print("Server started http://%s:%s" % (hostName, serverPort))
#     try:
#         webServer.serve_forever()
#     except KeyboardInterrupt:
#         pass
#
#     webServer.server_close()
#     print("Server stopped.")