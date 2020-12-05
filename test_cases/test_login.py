# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/11/29

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
from library.ddt import ddt, data
from main import run


# 从配置文件中获取用例excel名称
file_name = conf.get('excel', 'file_name')


@ddt
class LoginTestCase(unittest.TestCase):

    # 拼接完整的excel路径 读取数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), 'login')
    cases = wb.read_line_data()

    @classmethod
    def setUpClass(cls) -> None:
        output_log.info('================================== 开始执行登录接口测试 ==================================')
        cls.http = HTTPRequest()

    @classmethod
    def tearDownClass(cls) -> None:
        output_log.info('================================== 开始执行登录接口测试 ==================================')
        cls.http.close()

    @data(*cases)
    def test_login(self, case):

        # 拼接url
        url = conf.get('env', 'url') + case.url

        # 定义向excel回写数据时的row
        self.row = case.case_id + 1

        # 发起请求
        response = self.http.request(url=url, method=case.method, data=eval(case.request_data))
        time.sleep(2)

        # 以下打印内容会显示在html测试报告中
        print()
        print('请求地址--> {}'.format(url))
        print('请求参数--> {}'.format(case.request_data))
        print('期望的测试结果--> {}'.format(case.expected_data))
        print('服务器响应数据--> {}'.format(response.json()))

        res = response.json()

        # 登录成功时 将服务器返回的数据中的token去掉 再来断言
        if res.get('token'):
            res.pop('token')

        try:
            self.assertEqual(eval(case.expected_data), res)
        except AssertionError as e:
            result = 'FAIL'
            output_log.exception(e)
            # 抛出异常 脚本才会将该条用例识别成测试失败
            raise e
        else:
            result = 'PASS'
            output_log.info('预期结果: {}, 实际结果: {}， 断言结果: {}'.format(case.expected_data, res, result))
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
        run('test_login')
