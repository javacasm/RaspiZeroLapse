# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server

MAIN_TITLE_BASE = 'Video stream test'

camera_height = 720
camera_width = 1280  

SERVER_STREAMING_PORT = 8008


TEMPLATE_PAGE="""\
<html>
<head>
<title>%MAIN_TITLE%</title>
</head>
<body>
<center><h1>%MAIN_TITLE%</h1></center>
<center><img src="stream.mjpg" width="%RESOLUTION_WIDTH%" height="%RESOLUTION_HEIGHT%"></center>
</body>
</html>
"""

def getTitle():
    return MAIN_TITLE_BASE + '(' + str(camera_width) + 'x' + str(camera_height) + ')'

def getURL():
    return 'http://localhost:'  + str(SERVER_STREAMING_PORT) 

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

output = None

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        global output
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            # Update the proper widht & height
            PAGE = TEMPLATE_PAGE.replace('%MAIN_TITLE%',getTitle()).replace('%RESOLUTION_WIDTH%',str(camera_width)).replace('%RESOLUTION_HEIGHT$',str(camera_height))
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

camera_stream = None

def startStream():
    global output
    camera_stream = picamera.PiCamera(resolution=str(camera_width) + 'x' + str(camera_height), framerate = 24)
    output = StreamingOutput()
    #Uncomment the next line to change your Pi's Camera rotation (in degrees)
    #camera.rotation = 90
    camera_stream.start_recording(output, format='mjpeg')
    
    address = ('', SERVER_STREAMING_PORT)
    print('Listening @ ' + str(SERVER_STREAMING_PORT) + '(' + str(camera_width) + ',' + str(camera_height) + ')')
    print(getURL())
    server = StreamingServer(address, StreamingHandler)
#    server.serve_forever()
    print("end startStream")


def stopStream(): 
    if camera_stream != None:
        camera_stream.stop_recording()
        camera_stream = None