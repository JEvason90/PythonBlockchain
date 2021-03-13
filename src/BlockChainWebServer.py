#A P2P network taken form here:https://pypi.org/project/pyp2p/
# Intersetingly linked to this: https://storj.io/developers
# Oh and this bollocks here in the dht_ some shit about a medical centre??
# https://github.com/StorjOld

#With thanks to the following for the inspiration:
#https://gist.github.com/bradmontgomery/2219997
# https://www.youtube.com/watch?v=Rvfs6Xx3Kww&t=158s
#
#cron job service in linux
#https://stackoverflow.com/questions/1603109/how-to-make-a-python-script-run-like-a-service-or-daemon-in-linux

#Web Server stuff

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import BlockChain as bc
import requests
import sys
import socket
import time


class BlockchainSever(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        BlockChain.blockChain = bc.blockChain
        self.wfile.write(self.blockChainToString())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        nextBlock = bc.generateBlock(post_data)
        bc.addBlockToChain(nextBlock)
        BlockChain.blockChain = bc.blockChain
        self._set_headers()
        self.wfile.write(self.blockChainToString())
        
    def blockChainToString(self):
        s = []
        for x in range(len(bc.blockChain)):
            s.append(bc.blockChain[x].__dict__)
        
        return json.dumps(s)

class Server():
    connections = []
    peers = []

    def __init__(self,BlockChain):
        BlockChain.blockChain = bc.blockChain
        server_address = ('127.0.0.1', 8080)
        httpd = HTTPServer(server_address, BlockchainSever)
        print 'Starting Server'

        httpd.serve_forever()

        while True:
            c, a = httpd.socket.accept()
            self.connections.append(c)
            self.peers.append(a[0])


class BlockchainClient:

    def get(self):
        # api-endpoint
        URL = "http://localhost:8080"
        # sending get request and saving the response as response object
        try:
            r = requests.get(url = URL)
        except Exception as e:
            print("Error in the GET")
        # extracting data in json format
        data = r.json()
        # printing the output
        print(data)

    def post(self,dataToPost):
        API_ENDPOINT = "http://localhost:8080"
        
        # data to be sent to api
        data = dataToPost
        
        # sending post request and saving response as response object
        try:
            r = requests.post(url = API_ENDPOINT, data = data)
        except Exception as e:
            print("Error in the POST")
        # extracting response text 
        response = r.json()
        print(response)

class Client(BlockchainClient):
    def __init__(self):
        while True:
            BlockChain.blockChain = self.get()
            time.sleep(30)
            False

            

class P2P:
    peers = []

class BlockChain:
    blockChain = bc.blockChain

while True:
    try:
        client = Client()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Error, assuming there is no server moving on!")

    try:
        server = Server(BlockChain)
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)