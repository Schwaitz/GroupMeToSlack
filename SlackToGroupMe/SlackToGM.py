#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import requests
import sys


class request_handler(BaseHTTPRequestHandler):
    # GET request handler
    # What to do when someone accesses it in a browser
    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        message = "<h1>Slack -> GroupMe Web Server is up</h1>"

        self.wfile.write(bytes(message, "utf8"))
        return


    def create_bot(self, name, group_id):
        url = "https://api.groupme.com/v3/bots?token="
        token_path = "token.txt"
        file = open(self.token_path, "r")
        url += file.read()
        file.close()

        message = {
                    "bot" : {
                        "name" : name,
                        "group_id" : group_id
                        }
                    }

        requests.post(url, data=json.dumps(message))



    def add_assoc(data, sl_id):
        data["users"].append({"sl_id": sl_id, "bot_id": "null"})


    def update_assoc(data, bot_id):

        for item in data["users"]:
            if item["bot_id"] == "null":
                item["bot_id"] = bot_id


    def save_assoc(self, data):
        assoc_path = "assoc.json"

        with open(self.assoc_path, "a") as outfile:
            json.dump(data, outfile)
            outfile.close()



    # POST request handler
    # What to do when the webserver receives POST data
    def do_POST(self):

        log_path = "slack_log.txt"
        gm_url = "https://api.groupme.com/v3/bots/post"
        group_id = "29134104"
        sl_id = "914abbc04a6e31e12fd685e69c"



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


        if "response" not in data:
            assoc_path = "assoc.json"
            file = open(self.assoc_path, "r")
            decode = json.loads(file.read())
            file.close()

            if data["user_id"] not in decode:
                self.create_bot(self, data["name"], group_id)
                self.add_assoc(self, data["user_id"])
                message = { "text": "Creating associated bot for Slack user '" + str(data["user_name"]) + "'.", "bot_id": sl_id }
                requests.post(gm_url, data=json.dumps(message))
            else:
                text = data["text"]
                bot_id = "not set"

                for item in decode["users"]:
                    if item["sl_id"] == data["user_id"]:
                        bot_id = item["bot_id"]
                        break


                message = {
                    "text": text,
                    "bot_id" : bot_id
                          }

                requests.post(gm_url, data=json.dumps(message))
        else:
            self.update_assoc(self, data["response"]["bot"]["bot_id"])

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
