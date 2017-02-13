#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import re
import sys


class request_handler(BaseHTTPRequestHandler):

    # GET request handler
    # What to do when someone accesses it in a browser
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "<h1>GroupMe -> Slack Web Server is up</h1><br><h2>Log</h2><br><ul style='list-style-type: none; padding:0; margin:0;'>"

        # Get array from log
        file = open("/home/ubuntu/GMTS/log.txt", "r")
        log = file.readlines()
        file.close()

        # Write lines from log.txt to message
        for l in log:
            message += "<li>" + l + "</li>"

        message += "</ul>"



        self.wfile.write(bytes(message, "utf8"))
        return

    # POST request handler
    # What to do when the webserver receives POST data
    def do_POST(self):

        # Handle and format the data
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        jsonstring = str(self.data_string, "utf-8").strip()
        data = json.loads(jsonstring)

        # Print it to console
        print(json.dumps(data, sort_keys=True, indent=4))

        # Write it to log
        file = open("/home/ubuntu/GMTS/log.txt", "a")
        file.writelines(json.dumps(data, sort_keys=True, indent=4))
        file.write('\n\n')

        # Make sure the sender is not a bot
        if data["sender_type"] != "bot":


            # Easily changeable info
            channel = "#test"
            username = data["name"]
            text = data["text"]


            # Get secret url without publicly posting to GitHub
            file = open("/home/ubuntu/GMTS/url.txt")
            iw_url = file.read()
            file.close()


            # Optional JSON parameter of "icon_emoji": ":ghost:"


            # Build the message to send
            message= {
                "channel": channel,
                "username": username,
                "text": text
                      }


            # Post the message to the incoming webhook url
            requests.post(iw_url, data=json.dumps(message))


        return


def run():

    # Use the [1] argument for what port to listen on
    port = int(sys.argv[1])
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, request_handler)
    print('running server on port {}...'.format(port))
    httpd.serve_forever()


run()