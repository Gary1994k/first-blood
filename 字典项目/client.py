from socket import *
import sys
import getpass


def login(s):
    while True:
        u = input('用户名:')
        p = getpass.getpass('密码:')
        if (' ' in u) or (' ' in p):
            print('智障,用户名和密码不能有空格')
        data = 'L ' + u + ' ' + p
        s.send(data.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return u
        else:
            return


def register(s):
    while True:
        u = input('请输入用户名:')
        p = getpass.getpass()
        p1 = getpass.getpass('Again:')
        if (' ' in u) or (' ' in p):
            print('用户名和密码不允许有空格')
            continue
        if p1 != p:
            print('两次输入密码不一致')
            continue
        data = 'R ' + u + ' ' + p
        s.send(data.encode())
        # 等待回复
        data = s.recv(128).decode()
        if data == 'OK':
            return 0
        elif data == 'EXISTS':
            return 1
        else:
            return 2


def begin():
    print('********************************')
    print('|       请选择您的操作         |')
    print('|          [1]登陆             |')
    print('|          [2]注册             |')
    print('|          [3]退出             |')
    print('|                              |')
    print('********************************')


def lookup(s, name):
    while True:
        print('********************************')
        print('|请选择您的操作                |')
        print('|[1]查找单词                   |')
        print('|[2]查看历史记录               |')
        print('|[3]退出                       |')
        print('|                              |')
        print('********************************')
        try:
            cmd = int(input("输入选项>>"))
        except Exception as e:
            print("命令错误")
            continue
        if cmd == 1:
            query(s, name)
        elif cmd == 2:
            history(s, name)
        elif cmd == 3:
            return
        else:
            print('请输入正确选项')
            sys.stdin.flush()  # 清楚标准输入
            continue


def query(s, name):
    while True:
        word = input('单词:')
        if word == '##':
            break
        msg = 'Q ' + word + ' ' + name
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            data = s.recv(2048).decode()
            print(data)
        else:
            print('没有查询到该单词')


def history(s, name):
    msg = 'H ' + name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data == 'OK':
        while True:
            data = s.recv(1024).decode()
            if data == '##':
                break
            print(data)
    else:
        print('没有历史记录')


def main():
    s = socket()
    addr = ('127.0.0.1', 8888)
    try:
        s.connect(addr)
    except:
        sys.exit('连接服务端失败,退出客户端')
    while True:
        begin()
        try:
            cmd = input('请输入您的操作序号>>')
        except Exception as e:
            print('命令错误')
            continue
        if cmd == '1':
            name = login(s)
            if name:
                print('登陆成功')
                lookup(s, name)
            else:
                print('用户名或密码错误')

        elif cmd == '2':
            r = register(s)
            if r == 0:
                print('注册成功')
            elif r == 1:
                print('用户已存在')
            else:
                print('注册失败')
        elif cmd == '3':
            s.send(b'E')
            sys.exit('谢谢使用')
        else:
            print('您的操作有误,请重新输入')
            sys.stdin.flush()
            continue


if __name__ == '__main__':
    main()
