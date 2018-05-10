from http_protocol.BaseHttpData import *

class Response(BaseHttpData):

    def __init__(self):
        super(Response, self).__init__()
        self.isSend = False
        self.statusCode = None
        self.reasonPhrase = ""
        # set default value
        self.ver = 'HTTP/1.1'

    def setResponseCode(self, ver, code, reason):
        self.ver = ver
        self.statusCode = str(code)
        self.reasonPhrase = reason

    def setHeader(self, header):
        for t in header:
            self.header[t[0]] = t[1]
    
    def setContext(self, context):
        for c in context:
            if isinstance(c, str):
                self.context += bytes(c, encoding='utf-8')
            elif isinstance(c, bytes):
                self.context += c
            else:
                pass

    def __str__(self):
        return self.toString()

    def toString(self):
        res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + str(value) + '\r\n'
        res += '\r\n'
        try:
            res += self.context.decode('utf-8') + '\r\n'
        except:
            pass
            
        return res.encode('utf-8')

    def getHeader(self):
        res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + str(value) + '\r\n'
        res += '\r\n'
        return bytes(res, encoding='utf-8')
    
    def getContext(self):
        return self.context

