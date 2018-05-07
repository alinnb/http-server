from BaseHttpData import * 

class Response(BaseHttpData):
    statusCode = None
    statusText = ""

    def print(self):
        print("ver:", self.ver)
        print("statusCode:", self.statusCode)
        print("statusText:", self.statusText)
        for key, value in self.header.items():
            print("header:", key, value)
        print("context:", self.context)

    def toString(self):
        res = self.ver + ' ' + self.statusCode + ' ' + self.statusText + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + value + '\r\n'
        res += '\r\n'
        res += self.context + '\r\n'
        return res.encode('utf-8')