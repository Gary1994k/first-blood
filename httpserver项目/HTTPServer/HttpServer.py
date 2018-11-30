# coding=utf-8
"""
name: Teacher LZ
time: 2018-10-1
"""
from socket import *
import sys
import re
import time
from threading import Thread
from setting import *


class HTTPServer(object):
    """初始化创建服务器套接字"""

    def __init__(self, addr=('0.0.0.0', 80)):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.addr = addr
        self.bind(addr)
    # 绑定服务器地址

    def bind(self, addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)
    # HTTP服务器启动

    def serv_forever(self):
        self.sockfd.listen(10)
        print('Listen the port %d...' % self.port)
        while True:
            connfd, addr = self.sockfd.accept()
            print('Connect from', addr)
            handle_client = Thread(target=self.handle_request, args=(connfd,))
            handle_client.setDaemon(True)  # 防止产生僵尸进程，使其主进程退出未处理子进程
            handle_client.start()
    # 客户端请求函数

    def handle_request(self, connfd):
        # 接收浏览器请求
        request = connfd.recv(4096)
        # 解析请求内容
        request_lines = request.splitlines()
        # 获取请求行
        request_line = request_lines[0].decode()
        # 正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern, request_line).groupdict()
        except:
            # 获取响应内容
            response_handlers = "HHTP1.1 500 Server Error\r\n"
            response_handlers += '\r\n'
            response_body = 'Server Error'
            response = response_handlers + response_body
            connfd.send(response.encode())
            return
        # 将请求发给frame得到返回数据结果
        status, response_body = self.send_request(env['METHOD'], env['PATH'])
        # 根据响应码组织响应头内容
        response_headlers = self.get_headlers(status)
        # 将结果组织为http response 发送给客户端
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

        # 和框架frame交互 发送request获取response
        def send_request(self,method, path):
            s = socket()
            s.connect(frame_addr)

            # 向webframe发送method path
            s.send(method.endcode())
            time.sleep(0.1)
            s.send(path.endcode())

            status = s.recv(128).decode()
            response_body = s.recv(4096 * 10).decode()
            return status, response_body

        def get_headlers(self,status):
            if status == '200':
                response_headlers = 'HTTP/1.1 200 OK\r\n'
                response_headlers += '\r\n'
            elif status == '400':
                response_headlers = 'HTTP/1.1 404 Not Found\r\n'
                response_headlers += '\r\n'
            return response_headlers


if __name__ == '__main__':
    httpd = HTTPServer(ADDR)
    httpd.serv_forever()
