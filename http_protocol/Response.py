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
            res += key + ": " + value + '\r\n'
        res += '\r\n'
        res += self.context.decode('utf-8') + '\r\n'
            
        return res.encode('utf-8')

    # def getHeader(self):
    #     res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
    #     for key, value in self.header.items():
    #         res += key + ": " + value + '\r\n'
    #     res += '\r\n'
    
    # def getContext(self):
    #     return self.context

