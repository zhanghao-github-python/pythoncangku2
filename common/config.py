# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

E-mail: zh13997821732@163.com


================================================================================

"""


import configparser
import os

from common.constant import CONF_DIR


class ReadConfig(configparser.ConfigParser):

    def __init__(self):
        super().__init__()
        # 调用父类的__init__方法之后 可以使用read方法来读取配置文件
        self.read(os.path.join(CONF_DIR, 'env.ini'), encoding='utf8')
        version = self.get('env', 'version')
        if version == 'test':
            self.read(os.path.join(CONF_DIR, 'config_test.ini'), encoding='utf8')
        elif version == 'prod':
            self.read(os.path.join(CONF_DIR, 'config_prod.ini'), encoding='utf8')


conf = ReadConfig()


if __name__ == '__main__':
    url = conf.get('env', 'url')
    print(url)
