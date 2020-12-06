# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/12/6

E-mail: zh13997821732@163.com


================================================================================

"""

import random


# 获取随机的用户名，由6位包括数字，大写，小写字母组成
def get_random_name():
    name = ""
    for i in range(6):
        num = random.randint(0, 9)
        # num = chr(random.randint(48,57))  # ASCII表示数字
        letter = chr(random.randint(97, 122))  # 取小写字母
        Letter = chr(random.randint(65, 90))  # 取大写字母
        s = str(random.choice([num, letter, Letter]))
        name += s
    return name


# 生成随机的email
def get_random_email():
    email_num = ''
    for i in range(8):
        num = random.randint(0, 9)
        s = str(random.choice([num]))
        email_num += s
    email = email_num + '@qq.com'
    return email


if __name__ == '__main__':
    res = get_random_name()
    print(res)

    mail = get_random_email()
    print(mail)
