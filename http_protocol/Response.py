from http_protocol.BaseHttpData import *

class Response(BaseHttpData):

    def __init__(self):
        super(Response, self).__init__()
        self.statusCode = None
        self.reasonPhrase = ""

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

