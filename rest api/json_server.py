#!/usr/bin/python

# Simple python server translating python dicts to json

import BaseHTTPServer
import json
import os
import time

HOST_NAME="localhost"
PORT_NUMBER=8080
data = {}

class myServer(BaseHTTPServer.BaseHTTPRequestHandler):

  def do_GET(self):
    # GET received - check if we're delivering the entire payload
    if self.path == '/words':
      self.send_response(200)
      self.send_header("Content-type", "application/json")
      self.end_headers()
      self.wfile.write(json.dumps(data))
    # GET received - specified something other than /words
    elif os.path.basename(self.path) != "words":
      curr_word = os.path.basename(self.path)
      # Do we have this word?
      if curr_word in data:
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        single_return = {curr_word: data[curr_word]}
        self.wfile.write(json.dumps(single_return))
      # We do not have this word
      else:
        self.send_error(500, "Word curr_word not found.")
        self.send_header("Content-type", "text/html")
        self.end_headers()

  def do_PUT(self):
   
    # PUT received - check if we have something other than just /words
    if "/words/" in self.path:
      
      curr_word = os.path.basename(self.path) 
      # PUT received - Do we have the word we've received?
      if curr_word in data:
        # Increment count of this word
        data[curr_word] += 1
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
      # PUT received - We don't have this word, add it
      else:
        data[curr_word] = 1
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    else:
        self.send_error(500, "You must specify 1 word.")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.rfile.write('{"error": "PUT requests must be one word in length"}')


      
if __name__ == '__main__':
    # Instantiate our server
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), myServer)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
