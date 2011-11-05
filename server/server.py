#!/usr/bin/env python

from gevent.server import StreamServer
from config import HOST,PORT
from gevent import monkey; monkey.patch_all()
import json


CHUNK_BLOCK_SIZE = 4096

class SocketDisconnectedError(Exception):
    pass

class JsonServer(object):

    def __init__(self, socket, address):
        self.sock = socket
        self.address = address

    def onmessage(self, json_data):
        print json_data

    def __call__(self):
        recv_data = '' # received data
        while 1:
            
            #try to read some data block from 
            recv_data += self.sock.recv(CHUNK_BLOCK_SIZE)
            if recv_data == None:
                #TODO exit from routine, client is disconnected
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
    
    def response(self, data_to_send):
        " This function sends response to the client through socket connection "
        if type(data_to_send) == str:
            self.sock.send(data_to_send)
        elif type(data_to_send) == dict or type(data_to_send) == list:
            self.sock.send(json.dumps(data_to_send))
        else:
            raise ValueError('Wrong type of sent data')



def routine(socket, address):
    JsonServer(socket, address)()


if __name__ == '__main__':
    print "I'm here!!"
    server = StreamServer((HOST, PORT), routine)
    server.serve_forever()
