import socket

class BaseHttpData:
    ver = ""
    host = ""
    header = {}
    context = ""

class Request(BaseHttpData):
    method = ""
    uri = ""

    def print(self):
        print("method:", self.method)
        print("uri:", self.uri)
        print("ver:", self.ver)
        for key, value in self.header.items():
            print("header:", key, value)
        print("context:", self.context)

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

def httpParser(bStream, req):
    stream = bStream.decode('utf-8')
    strArray = stream.split("\r\n\r\n")
    #header
    headerArray = strArray[0].split("\r\n")
    for index,value in enumerate(headerArray):
        if index == 0:
            #method,uri,ver
            requestLineArray = value.split(" ")
            req.method = requestLineArray[0]
            req.uri = requestLineArray[1]
            req.ver = requestLineArray[2]
        else:
            headerLineArray = value.split(": ")
            headerKey = headerLineArray[0]
            headerValue = headerLineArray[1]
            req.header[headerKey] = headerValue
    
    #content
    if len(strArray) > 1:
        req.context = strArray[1]
    
    req.print()

def runServer():
    HOST, PORT = '', 8080

    listen_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, PORT))
    listen_socket.listen(1)

    print("Serving HTTP on port", PORT)
    while True:
        client_connection, client_address = listen_socket.accept()
        print("Connecting ",client_address)

        request = client_connection.recv(1024)
        print(request)
        
        req = Request()
        rsp = Response()

        httpParser(request, req)
        rsp.ver = req.ver
        rsp.statusCode = "200"
        rsp.statusText = 'OK'
        rsp.context = 'Hello World'

        client_connection.sendall(rsp.toString())
        client_connection.close()

def main():
    runServer()


main()