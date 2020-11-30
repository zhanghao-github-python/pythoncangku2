# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

E-mail: zh13997821732@163.com


================================================================================

"""

import os
# 文件或脚本文件路径 path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# 拼接路径 join
CONF_DIR = os.path.join(BASE_DIR, 'conf')

DATA_DIR = os.path.join(BASE_DIR, 'data')

LOGS_DIR = os.path.join(BASE_DIR, 'logs')

REPORTS_DIR = os.path.join(BASE_DIR, 'reports')

CASE_DIR = os.path.join(BASE_DIR, 'test_cases')


if __name__ == '__main__':

    print(BASE_DIR)
    print(DATA_DIR)
    print(CONF_DIR)
    print(LOGS_DIR)
    print(REPORTS_DIR)
    print(CONF_DIR)
