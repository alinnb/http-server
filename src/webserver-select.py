import select
import socket
import queue


class BaseHttpData:
    ver = ""
    host = ""
    header = {}
    context = ""

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

class HttpConnection:
    request = None
    response = None

    def __init__(self):
        self.request = Request()
        self.response = Response()

class WebServer:    
    server = None
    inputs = []
    outputs = []
    # message_queue = {}
    httpConnection = {}

    def __init__(self):
        print("WebServer init")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = ('127.0.0.1', 8080)
        self.server.bind(self.server_address)
        self.inputs = [self.server]

    def httpParser(self, bStream, req):
        try:
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

        except Exception as e:
            print("httpparser error", e)

        else:
            req.print() 

    def closeConnect(self, connect):
        if connect in self.outputs:
            self.outputs.remove(connect)
        self.inputs.remove(connect)
        connect.close()
        
    def start(self):
        self.server.listen(10)
        print("Serving ", self.server_address)

        timeout = 20

        while True:
            # print("Waiting for connection...")

            #select.select（rlist, wlist, xlist[, timeout]） 
            # 传递三个参数，
            #   一个为输入而观察的文件对象列表，
            #   一个为输出而观察的文件对象列表，
            #   一个观察错误异常的文件列表。
            #   第四个是一个可选参数，表示超时秒数。
            # 其返回3个tuple，
            #   每个tuple都是一个准备好的对象列表，它和前边的参数是一样的顺序。
            readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, timeout)

            if not (readable or writable or exceptional) :
                print("select 超时无活动连接， 重新select...")
                continue

            for s in readable:
                if s is self.server:
                    connect, client_address = s.accept()
                    print("new connection:", client_address)
                    connect.setblocking(0)

                    self.inputs.append(connect)
                    # message_queue[connect] = queue.Queue()
                    self.httpConnection[connect] = HttpConnection()

                else:
                    try:
                        data = s.recv(1024)
                    except ConnectionResetError as e:
                        print("connect error:", e)
                        self.closeConnect(s)
                    except Exception as e:
                        print("close connect:", e)
                        self.closeConnect(s)
                    else:
                        if data:
                            print("receive data:", data, "client:", s.getpeername())
                            # message_queue[s].put(data)
                            if s not in self.outputs:
                                self.outputs.append(s)

                            #parser the receive data
                            self.httpParser(data, self.httpConnection[s].request)

                        else:
                            print("close connect:", s.getpeername())
                            self.closeConnect(s)
                            # del message_queue[s]

            for s in writable:
                try:
                    # print("queue size",  message_queue[s].qsize())
                    # msg = message_queue[s].get_nowait()
                # except queue.Empty:
                #     err_msg = "connection" + str(s.getpeername()) + "output queue is empty."
                    self.httpConnection[s].response.ver = self.httpConnection[s].request.ver
                    self.httpConnection[s].response.statusCode = "200"
                    self.httpConnection[s].response.statusText = 'OK'
                    self.httpConnection[s].response.context = 'Hello World'
                    
                except Exception as e:
                    print("connection send data error", e)
                        # del message_queue[s]
                else:
                    print("generate response.", s.getpeername())
                    s.send(self.httpConnection[s].response.toString())
                
                if s in self.outputs:
                    self.outputs.remove(s)

            for s in exceptional:
                print("Excptional connection", s.getpeername())
                self.closeConnect(s)
                # del message_queue[s]

def main():
    server = WebServer()
    server.start()

main()
    



