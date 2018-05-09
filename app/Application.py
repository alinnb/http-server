
from file_system.file_helper import get_file
from http_protocol.status_codes import HTTP_STATUS_CODES

def application(environ, start_response):
    f = get_file(environ.request.absoluteURI)

    if f.exists:
        start_response('200 OK', [('Content-Type', f.mime_type), ('Content-Length', f.file_size)])
        return [f.read()]
    else:
        start_response('404 ' + HTTP_STATUS_CODES[404][0] , [])
        return HTTP_STATUS_CODES[404][1]

    return b''