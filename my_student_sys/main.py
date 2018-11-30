
from menu import show_menu
from student_info import *


def main():
    L = []
    while True:
        show_menu()
        s = input('请选择:')
        if s == 'q':
            break
        elif s == '1':
            L += input_student_info()
        elif s == '2':
            output_student_info(L)
        elif s == '3':
            delete_student_info(L)
        elif s == '4':
            modify_student_score(L)
        elif s == '5':
            print_info_by_score_desc(L)
        elif s == '6':
            print_info_by_score_asc(L)
        elif s == '7':
            print_info_by_age_desc(L)
        elif s == '8':
            print_info_by_age_asc(L)
        elif s == '9':
            save_student_file(L)
        elif s == '10':
            L = read_student_info()


if __name__ == '__main__':
    main()
