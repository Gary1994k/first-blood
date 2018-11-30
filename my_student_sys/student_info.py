
from student import Student


def input_student_info():
    L = []
    while True:
        n = input('请输入姓名:')
        if not n:
            break
        try:
            a = int(input('请输入年龄:'))
            s = int(input('请输入成绩:'))

        except:

            print('Please print it again !')
            continue
        L.append(Student(n, a, s))
    return L


def get_chinese_char_count(x):
    count = 0
    for ch in x:
        if ord(ch) > 127:
            count += 1
    return count


def output_student_info(L):
    print('+---------------+----------+----------+')
    print('|     name      |   age    |   score  |')
    print('+---------------+----------+----------+')
    for d in L:
        n, a, s = d.get_info()
        chinese_cnt = get_chinese_char_count(n)

        print('|%s|%s|%s|' % (n.center(15-chinese_cnt),
                              str(a).center(10), str(s).center(10)))
    print("+---------------+----------+----------+")


def delete_student_info(L):
    n = input('请输入要删除的学生的姓名: ')
    print('正在删除学生信息......', n)


def modify_student_score(L):
    print("正在修改学生成绩....")


def print_info_by_score_desc(L):
    def get_score(d):
        return d.get_score()
    L2 = sorted(L, key=get_score, reverse=True)
    output_student_info(L2)


def print_info_by_score_asc(L):
    def get_score(d):
        return d.get_score()
    L2 = sorted(L, key=get_score)
    output_student_info(L2)


def print_info_by_age_desc(L):
    def get_age(d):
        return d.get_age()
    L2 = sorted(L, key=get_age, reverse=True)
    output_student_info(L2)


def print_info_by_age_asc(L):
    def get_age(d):
        return d.get_age()
    L2 = sorted(L, key=get_age)
    output_student_info(L2)


def save_student_file(L, filename='si.txt'):
    import time
    print('正在保存信息......')
    time.sleep(2)
    try:
        f = open(filename, 'w')
        for d in L:
            d.save(f)
        f.close()
        print('保存信息成功......')
    except OSError:
        print('保存信息失败......')


def read_student_info(filename='si.txt'):
    import time
    print('正在读取数据......')
    time.sleep(2)
    L = []
    try:
        f = open('si.txt', 'rt')
        for line in f:
            n, a, s = line.strip().split(',')
            a = int(a)
            s = int(s)  # 转为整数
            L.append(Student(n, a, s))
        output_student_info(L)
        f.close()
        print('读取数据成功')
    except OSError:
        print('读取文件失败')
    return L