from socket import *
import os
import sys
import time
import signal
import pymysql

# 定义需要的全局变量
dict_text = './dict.txt'
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST, PORT)

# 流程控制


def main():
    # 创建数据库连接
    db = pymysql.connect('localhost', 'root',
                         '123456', 'dict')
    # 创建套接字
    s = socket()
    s.bind(ADDR)
    s.listen(5)
    # 忽略子进程信号
    signal.signal(signal.SIGCHLD, signal.SIG_IGN)
    while True:
        try:
            c, addr = s.accept()
            print('Connect from', addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        # 创建子进程
        pid = os.fork()
        if pid == 0:
            do_child(c, db)
        else:
            c.close()
            continue


def do_child(c, db):
    while True:
        msg = c.recv(128).decode()
        print(c.getpeername(), ":", msg)
        l = msg.split(' ')
        if (not l) or l[0] == 'E':
            c.close()
            sys.exit('客户端退出')
        elif l[0] == 'R':
            do_register(c, db, l[1], l[2])
        elif l[0] == 'L':
            do_login(c, db, l[1], l[2])
        elif l[0] == 'Q':
            do_query(c, db, l[1], l[2])
        elif l[0] == 'H':
            do_history(c, db, l[1])


def do_login(c, db, u, p):
    print('登陆操作')
    username = u
    password = p
    cursor = db.cursor()
    sql_c = "select * from user where name = '%s' and password = '%s'" % (
        username, password)
    cursor.execute(sql_c)
    r = cursor.fetchone()
    if r == None:
        c.send(b'FAIL')
    else:
        print('%s登陆成功' % username)
        c.send(b'OK')


def do_register(c, db, u, p):
    print('注册操作')
    username = u
    password = p
    cursor = db.cursor()
    sql_c = "select * from user where name='%s'" % username
    cursor.execute(sql_c)
    r = cursor.fetchone()
    if r != None:
        c.send(b'EXISTS')
        return
    else:
        sql_r = "insert into user (name,password) values('%s','%s')"\
            % (username, password)
        try:
            cursor.execute(sql_r)
            db.commit()
            c.send(b'OK')
        except:
            db.rollback()
            c.send('垃圾电脑,注册不了'.encode())
        else:
            print('%s注册成功' % username)


def do_query(c, db, word, username):
    print('查询操作')
    word = word
    name = username
    cursor = db.cursor()

    def insert_history():
        tm = time.ctime()
        sql = "insert into history (name,word,time) \
        values('%s','%s','%s')" % (name, word, tm)
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
    # 文本查询
    try:
        f = open(dict_text)
    except:
        c.send(b'FAIL')
        return

    for line in f:
        tmp = line.split(' ')[0]
        if tmp > word:
            c.send(b'FAIL')
            f.close()
            return
        elif tmp == word:
            c.send(b'OK')
            time.sleep(0.1)
            c.send(line.encode())
            f.close()
            insert_history()
            return
    c.send(b'FAIL')
    f.close()


def do_history(c, db, name):
    print('历史记录')
    name = name
    cursor = db.cursor()
    sql_c = "select * from history where name = '%s'" % name
    cursor.execute(sql_c)
    r = cursor.fetchall()
    if not r:
        c.send(b'FAIL')
        return
    else:
        c.send(b'OK')

    for i in r:
        time.sleep(0.1)
        msg = "%s    %s    %s" % (i[1], i[2], i[3])
        c.send(msg.encode())
    time.sleep(0.1)
    c.send(b'##')


if __name__ == '__main__':
    main()
