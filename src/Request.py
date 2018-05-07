from BaseHttpData import *


class Request(BaseHttpData):
    method = ""
    uri = ""

    def isValid(self):
        return self.method == "GET" or self.method == "POST"

    def print(self):
        print("method:", self.method)
        print("uri:", self.uri)
        print("ver:", self.ver)
        for key, value in self.header.items():
            print("header:", key, value)
        print("context:", self.context)
