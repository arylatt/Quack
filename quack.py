import http.server
import socketserver
import shutil
import os
import time
import sys
import json

if sys.argv[1] != "dev":
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

port = 8080

class QuackHandler(http.server.BaseHTTPRequestHandler):
    server_version = "Quack/2.0"

    def do_GET(self):
        f = self.send_head()
        if f:
            try:
                self.copyfile(f, self.wfile)
            finally:
                f.close()

    def do_HEAD(self):
        f = self.send_head()
        if f:
            f.close()

    def do_PUT(self):
        if self.path == "/quack":
            if self.headers['Authorization'] == "breakfast":
                with open('state.json') as json_file:
                    state = json.load(json_file)
                try:
                    if state['enabled'] == True:
                        if sys.argv[1] == "dev":
                            print("GPIO.output(12, GPIO.HIGH)")
                        else:
                            GPIO.output(12, GPIO.HIGH)
                        time.sleep(0.6)
                        if sys.argv[1] == "dev":
                            print("GPIO.output(12, GPIO.LOW)")
                        else:
                            GPIO.output(12, GPIO.LOW)
                        self.send_response(204, "NO CONTENT")
                        self.end_headers()
                    else:
                        self.send_error(503, "SERVICE UNAVAILABLE")
                except:
                    self.send_error(500, "INTERNAL SERVER ERROR")
            else:
                self.send_error(401, "UNAUTHORIZED")
        elif self.path == "/state":
            if self.headers['Authorization'] == 'BRECKFAST':
                self.send_response(http.server.HTTPStatus.OK)
                self.send_header("Content-type", "application/json")
                self.send_header("Content-Length", self.headers['Content-Length'])
                self.end_headers()
                payload = self.rfile.read(int(self.headers['Content-Length']))
                with open('state.json', 'wb') as f:
                    f.write(payload)
                self.wfile.write(payload)
            else:
                self.send_error(401, "UNAUTHORIZED")
        else:
            self.send_error(404, "NOT FOUND")

    def send_head(self):
        f = None
        self.send_response(http.server.HTTPStatus.OK)
        if self.path == "/duck.png":
            f = open('duck.png', 'rb')
            self.send_header("Content-type", 'image/png')
        elif self.path == "/state":
            f = open('state.json', 'rb')
            self.send_header("Content-type", "application/json")
        else:
            f = open('quack.html', 'rb')
            self.send_header("Content-type", 'text/html')
        try:
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def copyfile(self, source, outputfile):
        shutil.copyfileobj(source, outputfile)

handler = QuackHandler

with http.server.HTTPServer(("", port), handler) as httpd:
    print("running @ " + str(port))
    httpd.serve_forever()