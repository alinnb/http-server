
from http_protocol.Request import Request
from http_protocol.Response import Response
import config
import time

from enum import Enum

class ConnectionLifeCycle(Enum):
    dealing = 1
    waiting = 2

class HttpConnection:
    
    def __init__(self, application):
        self.request = Request()
        self.response = Response()
        self.application = application
        # self.keepAlive = config.KEEPALIVE
        # self.keepAlive_timeout = config.KEEPALIVE_TIMEOUT
        # self.keepAlive_countdown = time.time()
        # self.state = ConnectionLifeCycle.dealing

    def processer(self, connect, buffer):
        print(id(connect), connect.getpeername(), "receive data:", buffer)
        self.request.httpParser(buffer)
        self.response.setContext(self.application(self.request, self.response))

    def sendResponse(self, connect):
        try:
            print(id(connect), connect.getpeername(), "send response: ",  self.response.toString())
            connect.sendall(self.response.getHeader())
            connect.sendall(self.response.getContext())
        except:
            raise