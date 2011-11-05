#!/usr/bin/env python

from connection import Connection
from commands import handle_request

from gevent.server import StreamServer
from config import HOST,PORT
from gevent import monkey; monkey.patch_all()

import json


CHUNK_BLOCK_SIZE = 4096

class SocketDisconnectedError(Exception):
    pass

class JsonServer(object):

    def __init__(self, socket, address):
        self.address = address
        self.sock = socket
        self.connection = Connection(socket)
        print "Kitten has been borned"

    def onmessage(self, json_data):
        handle_request(json_data, self.connection)

    def __call__(self):
        recv_data = '' # received data
        while 1:
            #try to read some data block from 
            recv_data += self.sock.recv(CHUNK_BLOCK_SIZE)
            if recv_data == '':
                #TODO exit from routine, client is disconnected
                print "Kitten is dead"
                return
            try:
                # Try to loads gotten data into json
                json_data = json.loads(recv_data)
            except ValueError:
                # it's uncomplete json object, try to get data from socket again
                continue
            recv_data = ''
            try:
                self.onmessage(json_data)
            except SocketDisconnectedError:
                # End agian connection is lost
                return

def routine(socket, address):
    JsonServer(socket, address)()


if __name__ == '__main__':
    print "I'm here!!"
    server = StreamServer((HOST, PORT), routine)
    server.serve_forever()
