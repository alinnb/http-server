from http_protocol.BaseHttpData import *

class Response(BaseHttpData):

    def __init__(self):
        super(Response, self).__init__()
        self.statusCode = None
        self.reasonPhrase = ""

    # def print(self):
    #     print("ver:", self.ver)
    #     print("statusCode:", self.statusCode)
    #     print("reasonPhrase:", self.reasonPhrase)
    #     for key, value in self.header.items():
    #         print("header:", key, value)
    #     print("context:", self.context)

    def toString(self):
        res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + value + '\r\n'
        res += '\r\n'
        res += self.context + '\r\n'
        return res.encode('utf-8')
