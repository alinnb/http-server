import os

PORT = 8080

HOST = "127.0.0.1"

SOCKET_BACKLOG_SIZE = 5

ROOT = os.path.join(os.getcwd() + "/static/")

KEEPALIVE = True

KEEPALIVE_TIMEOUT = 10 * 1000 #ms

pass