from http_server.WebServer import WebServer
from app.Application import application

server = WebServer()
server.start(application)