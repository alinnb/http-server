from http_protocol.BaseHttpData import *
import os.path
import config

class Request(BaseHttpData):

    def __init__(self):
        super(Request, self).__init__()
        self.method = ""
        self.uri = ""
        self.absoluteURI = ""

    def isValid(self):
        return self.method == "GET" or self.method == "POST"

    # def print(self):
    #     print("method:", self.method)
    #     print("uri:", self.uri)
    #     print("ver:", self.ver)
    #     for key, value in self.header.items():
    #         print("header:", key, value)
    #     print("context:", self.context)

    def httpParser(self, bStream):
        try:
            strArray = bStream.decode('utf-8').split("\r\n\r\n")
            #header
            headerArray = strArray[0].split("\r\n")
            for index, value in enumerate(headerArray):
                if index == 0:
                    #method,uri,ver
                    requestLineArray = value.split(" ")
                    self.method = requestLineArray[0]
                    self.uri = requestLineArray[1]
                    self.ver = requestLineArray[2]
                else:
                    headerLineArray = value.split(": ")
                    headerKey = headerLineArray[0]
                    headerValue = headerLineArray[1]
                    self.header[headerKey] = headerValue

            #content
            if len(strArray) > 1:
                self.context = strArray[1]

        except Exception as e:
            print("httpparser error", e)
        # 生成绝对路径
        self.absoluteURI = os.path.abspath(config.ROOT + self.uri)