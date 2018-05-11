from http_server.httpserver_select import WebServer
from app.Application import application
import config

httpd = WebServer(config.HOST, config.PORT, application)
httpd.serve_forever()