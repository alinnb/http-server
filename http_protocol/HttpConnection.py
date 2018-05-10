
from http_protocol.Request import Request
from http_protocol.Response import Response

import config
import time

class HttpConnection:
    
    def __init__(self, application):
        self.responseList = []
        self.application = application

        self.keepAlive = config.KEEPALIVE
        self.keepAlive_timeout = config.KEEPALIVE_TIMEOUT
        self.keepAlive_stamp = time.time()
        self.keepAlive_max = config.KEEPALIVE_MAX

    def processer(self, connect, buffer):
        print(id(connect), connect.getpeername(), "receive data:", buffer)

        req = Request()
        req.httpParser(buffer)
        
        rsp = Response()
        rsp.request = req
        rsp.setContext(self.application(req, rsp))
        
        # deal keep-alive
        if self.keepAlive:
            self.keepAlive_max -= 1
            if self.keepAlive_max == 0:
                rsp.setHeader([('Connection', 'close')])
            else:
                rsp.setHeader([('Connection', 'keep-alive'), ('Keep-Alive', 'timeout = %d, max = %d' % (self.keepAlive_timeout, self.keepAlive_max))])

        self.responseList.append(rsp)

    def sendResponse(self, connect, close):
        while len(self.responseList) > 0:
            rsp = self.responseList.pop(0)
            try:
                print(id(connect), connect.getpeername(), "send response: ",  rsp.toString())
                connect.sendall(rsp.getHeader())
                connect.sendall(rsp.getContext())
            except:
                raise

        if (not self.keepAlive) or (self.keepAlive_max <= 0 or time.time() - self.keepAlive_stamp > self.keepAlive_timeout):
            close(connect)
