#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import sys



class request_handler(BaseHTTPRequestHandler):
    # GET request handler
    # What to do when someone accesses it in a browser
    log_path = "log.txt"
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "<h1>GroupMe -> Slack Web Server is up</h1><br><h2>Log</h2><br><ul style='list-style-type: none; padding:0; margin:0;'>"

        # Get array from log
        file = open(self.log_path, "r")
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
        file = open(self.log_path, "a")
        file.writelines(json.dumps(data, sort_keys=True, indent=4))
        file.write('\n\n')

        # Make sure the sender is not a bot
        if data["sender_type"] != "bot":


            # Easily changeable info
            channel = "#test"
            username = data["name"]
            text = data["text"]
            avatar = data["avatar_url"]

            if username is "GroupMe":
                avatar = "http://i.imgur.com/8xeeQ2A.png"
            if avatar is "null":
                avatar = "http://i.imgur.com/8xeeQ2A.png"


            # Get secret url without publicly posting to GitHub
            file = open(self.log_path)
            iw_url = file.read()
            file.close()




            # Build the message to send
            message= {
                "channel": channel,
                "username": username,
                "text": text,
                "icon_url" : avatar
                      }


            # Post the message to the incoming webhook url
            requests.post(iw_url, data=json.dumps(message))


        return


def run():

    # Use the [1] argument for what port to listen on
    port = "8080"
    try:
        port = sys.argv[1]
    except IndexError:
        print("using default port, " + port)

    server_address = ('0.0.0.0',int(port))
    httpd = HTTPServer(server_address, request_handler)
    print('running server on port {}...'.format(port))
    httpd.serve_forever()

if __name__ == '__main__':
    run()
