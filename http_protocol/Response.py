
from http_protocol.BaseHttpData import *

import config
import queue
import struct

if config.CONTENT_ENCODING == 'gzip':
    import gzip


class Response(BaseHttpData):

    def __init__(self):
        super(Response, self).__init__()
        self.isSend = False
        self.statusCode = None
        self.reasonPhrase = ""
        self.request = None
        self.isChunk = False
        self.chunkQueue = queue.Queue()
        self.chunkFinish = False
        self.headerSent = False
        # set default value
        self.ver = 'HTTP/1.1'

    def setResponseCode(self, ver, code, reason):
        self.ver = ver
        self.statusCode = str(code)
        self.reasonPhrase = reason

    def setHeader(self, header):
        for t in header:
            self.header[t[0]] = t[1]
    
    def removeHeader(self, header):
        for t in header:
            if t in self.header:
                self.header.pop(t)

    def setContext(self, context):
        for c in context:
            if isinstance(c, str):
                self.context += bytes(c, encoding='utf-8')
            elif isinstance(c, bytes):
                self.context += c
            else:
                pass

        for e in self.request.encodingQValue:
            if e[0].lower() == 'gzip' and config.CONTENT_ENCODING == 'gzip':
                self.context = gzip.compress(self.context)
                self.setHeader([('Content-Encoding', e[0])])
            # if e[0].lower() == 'compress':
            #     return f.read()
            # if e[0].lower() == 'deflate':
            #     return f.read()

        self.setHeader([('Content-Length', len(self.context))])

    def setKeepAlive(self, timeout, max):
        if max == 0:
            self.setHeader([('Connection', 'close')])
        else:
            self.setHeader([('Connection', 'keep-alive'), ('Keep-Alive', 'timeout = %d, max = %d' % (timeout, max))])

    def checkTransferChunked(self):
        if self.isChunk:
            self.setHeader([('Transfer-Encoding', 'chunked')])
            self.setHeader([('Connection', 'close')])
            self.removeHeader(['Content-Length'])
            self.removeHeader(['Keep-Alive'])

    def __str__(self):
        return self.toString()

    def toString(self):
        res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + str(value) + '\r\n'
        res += '\r\n'
        try:
            if not self.isChunk:
                res += self.context.decode('utf-8') + '\r\n'
        except:
            pass

        return res.encode('utf-8')

    def getHeader(self):
        res = 'HTTP/1.1' + ' ' + self.statusCode + ' ' + self.reasonPhrase + '\r\n'
        for key, value in self.header.items():
            res += key + ": " + str(value) + '\r\n'
        res += '\r\n' #blank line
        return bytes(res, encoding='utf-8')

    def getContext(self):
        return self.context

    # def getChunkGenerator(self):
    #     yield b'B\r\nhello,world\r\n'
    #     s = '看起来A、B的执行有点像多线程，但协程的特点在于是一个线程执行，那和多线程比，协程有何优势？'
    #     buffer = bytes(s, encoding='utf-8')
    #     yield b'%x'%len(buffer) + b'\r\n' + buffer + b'\r\n'
    #     buffer = b'world'
    #     yield b'%x'%len(buffer) + b'\r\n' + buffer + b'\r\n'
    #     yield b'0\r\n'
    #     yield b'\r\n'
    #     return b''

    def getChunk(self):
        buffer = b''
        try:
            task = self.chunkQueue.get_nowait()
            self.chunkQueue.task_done()

            if not task:
                self.chunkFinish = True
                return b'0\r\n\r\n'

            buffer += task

        except queue.Empty:
            raise

        except Exception as e:
            print("Something wrong" + str(e))

        print("[Send Chunk] ", len(buffer))
        return b'%x'%len(buffer) + b'\r\n' + buffer + b'\r\n'
