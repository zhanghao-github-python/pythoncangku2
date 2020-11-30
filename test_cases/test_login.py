# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

E-mail: zh13997821732@163.com


================================================================================

"""
import os

from common.constant import DATA_DIR
from common.config import conf
file_path = os.path.join(DATA_DIR, 'api_automation.course.xlsx')
print(file_path)

url = conf.get('env', 'url') + '/user/login/'
print(url)
