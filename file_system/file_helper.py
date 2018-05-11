
import os
import mimetypes

import threading
import queue

class AsyncFileHelper(threading.Thread):
    def __init__(self, absoluteURI, queue):
        threading.Thread.__init__(self)  
        self.absoluteURI = absoluteURI
        self.queue = queue

    def run(self):
        try:
            fn = open(self.absoluteURI, 'rb')
            while True:
                buffer = fn.read(1024 * 1024)
                if not buffer:
                    self.queue.put_nowait(b'')
                    break
                else:
                    print("put size: " +  str(len(buffer)))
                    self.queue.put_nowait(buffer)

            print("waiting for finish...")
            self.queue.join()
        except Exception as e:
            print("error to reading file async " +  self.absoluteURI + " " + str(e))
        print("AsyncFileHelper finished.")

class File:
    def __init__(self, absoluteURI=None, file_name=None, file_size=None, exists=False, mime_type=None):
        self.absoluteURI = absoluteURI
        self.file_name = file_name
        self.file_size = file_size
        self.exists = exists
        self.mime_type = mime_type

    def __str__(self):
        return 'File (request_uri=%s, file_name=%s, exists=%s, mime_type=%s)' % \
               (self.absoluteURI, self.file_name, self.exists, self.mime_type)

    def read(self):
        with open(self.absoluteURI, 'rb') as f:
            return f.read()

        return b""

    # def readCoroutie(self):


    def readAsync(self, queue):
        f = AsyncFileHelper(self.absoluteURI, queue)
        f.start()

def get_file(absoluteURI):

    fn = absoluteURI
    file_name = None
    mime_type = None
    file_size = None
    exists = False
    try:
        if os.path.isfile(fn):
            path, file_name = os.path.split(absoluteURI)
            file_size = os.path.getsize(fn)
            exists = True
            type, encoding = mimetypes.guess_type(fn)
            if type:
                mime_type = type

    except:
        pass

    return File(absoluteURI, file_name, file_size, exists, mime_type)

if __name__ == '__main__':
    fn = os.path.abspath('./static/1.MP4')
    f = get_file(fn)
    q = queue.Queue()
    f.readAsync(q)

    totalSize = 0
    while True:
        try:
            task = q.get_nowait()
            q.task_done()

            if not task:
                print("work finished! " + str(totalSize))
                break

            print("working " +  str(len(task)))
            totalSize += len(task)

        except queue.Empty:
            print("no work?")

        except Exception as e:
            print("Something wrong" + str(e))