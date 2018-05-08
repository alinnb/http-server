# 使用python内置的WSGI服务器  
from wsgiref.simple_server import make_server  
  
def application(environ, start_response):  
   # 排序并将环境字典的键值对转换为字符串  
   response_body = ['%s: %s' % (key, value)  
                    for key, value in sorted(environ.items())]  
   response_body = '\n'.join(response_body)  
  
   status = '200 OK'  
   response_headers = [('Content-Type', 'text/plain'),  
                  ('Content-Length', str(len(response_body)))]  
   start_response(status, response_headers)  
  
   return [response_body]  
  
# 实例化一个WSGI服务器对象。  
# 该服务器对象可以接收来自客户端（我们的浏览器）的请求，将它传给应用程序，  
# 并且将应用程序返回过来的响应再发送给客户端。  
httpd = make_server(  
   'localhost', # 主机名。  
   8051, # 监听请求的端口号。  
   application # 我们的可调用应用对象，在这里是一个函数。  
   )  
  
# 在这里简单地一次性监听，得到响应后处理完则直接退出。  
httpd.handle_request()  