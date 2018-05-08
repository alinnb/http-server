
from http_protocol.Request import Request
from http_protocol.Response import Response

class HttpConnection:
    request = None
    response = None
    state = ""

    def __init__(self):
        self.request = Request()
        self.response = Response()
        self.state = "init"

    def start_response(self, code, header):
        if self.state == "init":
            self.response.ver = self.request.ver
            self.response.statusCode = code.split(' ')[0]
            self.response.statusText = code.split(' ')[1]
            for t in header:
                self.response.header[t[0]] = t[1] #切片
            self.state = "header finish"
    
    def setContext(self, context):
        if self.state == "header finish":
            for c in context:
                self.response.context += c.decode('utf-8')
            self.state = "context finish"

    def sendFinish(self):
        if self.state == "context finish":
            self.state = "send finish"

    def isFinish(self):
        return self.state == "send finish"
        
        