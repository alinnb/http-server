
from file_system.file_helper import get_file
from http_protocol.status_codes import HTTP_STATUS_CODES

def application(request, response):
    f = get_file(request.absoluteURI)
    code = None

    if f.exists:
        code = 200
    else:
        code = 404
    
    response.setResponseCode(request.ver, code, HTTP_STATUS_CODES[code][0])
    
    if f.exists:
        response.setHeader([('Content-Type', f.mime_type), ('Content-Length', f.file_size)])
        return [f.read()]
    
    return HTTP_STATUS_CODES[code][1]