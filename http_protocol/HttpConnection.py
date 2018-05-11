
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
            rsp.setKeepAlive(self.keepAlive_timeout, self.keepAlive_max)

        # check transfer chunked
        rsp.checkTransferChunked()

        self.responseList.append(rsp)

    def sendResponse(self, connect, close):
        while len(self.responseList) > 0:
            rsp = self.responseList[0]
            try:
                if not rsp.headerSent:
                    print(id(connect), connect.getpeername(), "send response: ",  rsp.toString())
                    connect.sendall(rsp.getHeader())
                    rsp.headerSent = True

                if not rsp.isChunk:
                    connect.sendall(rsp.getContext())
                else:# chunk transfering
                    connect.sendall(rsp.getChunk())
                    if not rsp.chunkFinish:
                        return

                self.responseList.pop(0)
            except:
                raise

        if (not self.keepAlive) or (self.keepAlive_max <= 0 or time.time() - self.keepAlive_stamp > self.keepAlive_timeout):
            close(connect)
