import http.server
import socketserver
import shutil
import os
import time
import RPi.GPIO as GPIO

port = 8080

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT, initial=GPIO.LOW)

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
                GPIO.output(12, GPIO.HIGH)
                time.sleep(0.6)
                GPIO.output(12, GPIO.LOW)
                self.send_response(204, "NO CONTENT")
                self.end_headers()
            else:
                self.send_error(401, "UNAUTHORIZED")
        else:
            self.send_error(404, "NOT FOUND")

    def send_head(self):
        f = None
        self.send_response(http.server.HTTPStatus.OK)
        if self.path == "/duck.png":
            f = open('duck.png', 'rb')
            try:
                self.send_header("Content-type", 'image/png')
                fs = os.fstat(f.fileno())
                self.send_header("Content-Length", str(fs[6]))
                self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
                self.end_headers()
                return f
            except:
                f.close()
                raise
        else:
            f = open('quack.html', 'rb')
            try:
                self.send_header("Content-type", 'text/html')
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