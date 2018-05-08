from http_protocol.BaseHttpData import *

class Request(BaseHttpData):

    def __init__(self):
        super(Request, self).__init__()
        self.method = ""
        self.uri = ""

    def isValid(self):
        return self.method == "GET" or self.method == "POST"

    # def print(self):
    #     print("method:", self.method)
    #     print("uri:", self.uri)
    #     print("ver:", self.ver)
    #     for key, value in self.header.items():
    #         print("header:", key, value)
    #     print("context:", self.context)
