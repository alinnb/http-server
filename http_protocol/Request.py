from http_protocol.BaseHttpData import *
import os.path
import config

class Request(BaseHttpData):

    def __init__(self):
        super(Request, self).__init__()
        self.method = ""
        self.uri = ""
        self.absoluteURI = ""
        self.query = {}
        self.cookies = {}

    def isValid(self):
        return self.method == "GET" or self.method == "POST"

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
                    if self.uri.find('?') >= 0:
                        uriArray = self.uri.split('?')
                        self.uri = uriArray[0]
                        self.setQueryString(uriArray[1])
                    self.ver = requestLineArray[2]
                else:
                    headerLineArray = value.split(": ")
                    headerKey = headerLineArray[0]
                    headerValue = headerLineArray[1]
                    self.header[headerKey] = headerValue
                    if headerKey == 'Cookie':
                        self.setCookieString(headerValue)

            #content
            if len(strArray) > 1:
                self.context = strArray[1]

        except Exception as e:
            print("httpparser error", e)
        # 生成绝对路径
        self.absoluteURI = os.path.abspath(config.ROOT + self.uri)

    def setQueryString(self, Stream):
        try:
            queryArray = Stream.split('&')
            for q in queryArray:
                qArray = q.split('=')
                self.query[qArray[0]] = qArray[1]
        except:
            pass

        # for k,q in self.query.items():
        #     print("query:", k, q)
    
    def setCookieString(self, Stream):
        try:
            cookieArray = Stream.split(';')
            for c in cookieArray:
                i = c.find('=')
                if i >= 1:
                    self.cookies[c[:i-1].strip()] = c[i+1:].strip()
        except:
            pass

        # for k,q in self.cookies.items():
        #     print("cookie:", k, q)