
import os
import mimetypes

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

    def read_size(self, response):
        try:
            fn = open(self.absoluteURI, 'rb')
            while True:
                buffer = fn.read(1024)
                if not buffer:
                    break
                else:
                    response.context += buffer
        except:
            pass

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

    