import select
import socket
import queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(False)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_address = ('127.0.0.1', 8080)
server.bind(server_address)
server.listen(10)
print("Serving ", server_address)


inputs = [server]
outputs = []
message_queue = {}
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
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)

    if not (readable or writable or exceptional) :
        print("select 超时无活动连接， 重新select...")
        continue

    for s in readable:
        if s is server:
            connect, client_address = s.accept()
            print("new connection:", client_address)
            connect.setblocking(0)

            inputs.append(connect)
            message_queue[connect] = queue.Queue()

        else:
            try:
                data = s.recv(1024)
            except:
                err_msg = "client Error" + s.getpeername()
                
            if data:
                print("receive data:", data, "client:", s.getpeername())
                message_queue[s].put(data)
                if s not in outputs:
                    outputs.append(s)
            else:
                print("close connect:", s.getpeername())
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queue[s]

    for s in writable:
        try:
            # print("queue size",  message_queue[s].qsize())
            msg = message_queue[s].get_nowait()
        except queue.Empty:
            err_msg = "connection" + str(s.getpeername()) + "output queue is empty."
        except Exception as e:
            print("connection send data error", e)
            if s in outputs:
                outputs.remove(s)
                del message_queue[s]
        else:
            print("send data", msg, "to", s.getpeername())
            s.send(msg)

    for s in exceptional:
        print("Excptional connection", s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queue[s]




