# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/12/6

E-mail: zh13997821732@163.com


================================================================================

"""
import os
import sys
import time
import unittest

sys.path.append('..')

from common.constant import DATA_DIR, CASE_DIR
from common.config import conf
from common.read_excel import ReadExcel
from common.logger import output_log
from common.http_request import HTTPRequest
from common.execute_mysql import ExecuteMysql
from library.ddt import ddt, data
from main import run
from common.tools import get_random_email, get_random_name


# 从配置文件中获取用例excel名称
file_name = conf.get('excel', 'file_name')


@ddt
class LoginTestCase(unittest.TestCase):

    # 拼接完整的excel路径 读取数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), 'register')
    cases = wb.read_line_data()

    @classmethod
    def setUpClass(cls) -> None:
        output_log.info('================================== 开始执行注册接口测试 ==================================')
        cls.http = HTTPRequest()
        cls.db = ExecuteMysql()

    @classmethod
    def tearDownClass(cls) -> None:
        output_log.info('================================== 开始执行注册接口测试 ==================================')
        cls.http.close()

    @data(*cases)
    def test_register(self, case):

        # 拼接url
        url = conf.get('env', 'url') + case.url

        # 定义向excel回写数据时的row
        self.row = case.case_id + 1

        # 先取出请求数据
        request_data = eval(case.request_data)
        if request_data.get('username') == '$username':
            username = get_random_name()
            request_data['username'] = username
        else:
            username = request_data['username']
        if request_data.get('email') == '$email':
            email = get_random_email()
            request_data['email'] = email
        else:
            email = request_data['email']


        # 发起请求
        response = self.http.request(url=url, method=case.method, data=request_data)
        time.sleep(2)

        # 以下打印内容会显示在html测试报告中
        print()
        print('请求地址--> {}'.format(url))
        print('请求参数--> {}'.format(case.request_data))
        print('期望的测试结果--> {}'.format(case.expected_data))
        print('服务器响应数据--> {}'.format(response.json()))

        res = response.json()

        # 注册成功时 将服务器返回的数据中的token去掉 再来断言
        if res.get('token'):
            res.pop('token')

        # 获取注册之后的账户的id
        sql = "SELECT id FROM auth_user WHERE username='{}';".format(username)
        uid = self.db.find_one(sql=sql)[0]

        if res.get('id'):
            # 组装期望结果
            expected_data = {'id': uid, 'username': username}
        else:
            expected_data = eval(case.expected_data)

        try:
            self.assertEqual(expected_data, res)
        except AssertionError as e:
            result = 'FAIL'
            output_log.exception(e)
            # 抛出异常 脚本才会将该条用例识别成测试失败
            raise e
        else:
            result = 'PASS'
            output_log.info('预期结果: {}, 实际结果: {}， 断言结果: {}'.format(expected_data, res, result))
        finally:
            # 向excel回写数据
            self.wb.write_data(row=self.row, column=9, value=str(response.json()))
            self.wb.write_data(row=self.row, column=10, value=result)


if __name__ == '__main__':
    env = conf.get('env', 'env')
    if env == 'all':
        run(CASE_DIR)
    elif env == 'one':
        # 命令行执行该测试脚本所有用例 python test_login.py
        run('test_register')
