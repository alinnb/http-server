import select
import socket
import queue
import errno
import time

from http_protocol.Request import Request
from http_protocol.Response import Response
from http_protocol.HttpConnection import HttpConnection

class WebServer:
    server = None
    application = None
    inputs = []
    outputs = []
    httpConnections = {}
    
    def __init__(self, host, port, application):
        print("WebServer init")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setblocking(False)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_address = (host, port)
        self.server.bind(self.server_address)
        self.inputs = [self.server]
        self.application = application

    def closeConnect(self, connect):
        print(id(connect), connect.getpeername(), "connection closed")
        if connect in self.outputs:
            self.outputs.remove(connect)
        self.inputs.remove(connect)
        connect.close()

    def serve_forever(self):
        self.server.listen(10)
        print("Serving HTTP on", self.server_address)

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
            readable, writable, exceptional = select.select(
                self.inputs, self.outputs, self.inputs, timeout)

            if not (readable or writable or exceptional):
                # print("select 超时无活动连接， 重新select...")
                continue

            for s in readable:
                if s is self.server:
                    connect, client_address = s.accept()
                    print(id(connect), client_address, "new connection")
                    connect.setblocking(False)

                    self.inputs.append(connect)
                    self.httpConnections[connect] = HttpConnection(self.application)

                else:
                    buffer = b''
                    try:
                        # 设置socket为非租塞模式，读取需要处理的异常。 socket.setblocking(False)
                        # 其中err == errno.EAGAIN or err == errno.EWOULDBLOCK不是真正的异常，只是数据读完了
                        while True:
                            try:
                                data = s.recv(1024)
                            except socket.error as e:
                                err = e.args[0]
                                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                                    # print('Socket s No data available')
                                    break
                                else:
                                    raise
                            else:
                                if len(data) == 0:
                                    break
                                buffer += data

                    except socket.error as e:
                        print("socket.error:", str(e))
                        err = e.args[0]
                        self.closeConnect(s)
                    except Exception as e:
                        print("close connect:", e)
                        self.closeConnect(s)
                    else:
                        if buffer:
                            self.httpConnections[s].processer(s, buffer)
                            if s not in self.outputs:
                                self.outputs.append(s)
                        else:
                            print(id(connect), connect.getpeername(), "receive data: EOF")
                            self.closeConnect(s)

            for s in writable:
                try:
                    self.httpConnections[s].sendResponse(s, self.closeConnect)
                except Exception as e:
                    print("connection send data error", e)
                    self.closeConnect(s)

            for s in exceptional:
                print(id(s), s.getpeername(), "Excptional connection")
                self.closeConnect(s)

if __name__ == '__main__':
    from app.Application import application
    server = WebServer('127.0.0.1', 8080, application)
    server.serve_forever()
