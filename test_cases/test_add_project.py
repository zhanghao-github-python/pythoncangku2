# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/12/12

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
from common.tools import get_token, get_random_name

# 从配置文件中获取用例excel名称
file_name = conf.get('excel', 'file_name')


@ddt
class ProjectTestCase(unittest.TestCase):
    # 拼接完整的excel路径 读取数据
    wb = ReadExcel(os.path.join(DATA_DIR, file_name), 'project')
    cases = wb.read_line_data()

    @classmethod
    def setUpClass(cls) -> None:
        output_log.info('================================== 开始执行增加项目接口测试 ==================================')
        cls.http = HTTPRequest()

    @classmethod
    def tearDownClass(cls) -> None:
        output_log.info('================================== 开始执行增加项目接口测试 ==================================')
        cls.http.close()

    @data(*cases)
    def test_add_project(self, case):

        # 拼接url
        url = conf.get('env', 'url') + case.url

        # 定义向excel回写数据时的row
        self.row = case.case_id + 1
        request_data = eval(case.request_data)
        if request_data.get('name') == '$name':
            name = get_random_name()
            request_data['name'] = name
        else:
            name = request_data['name']

        token = get_token(eval(case.token_data))
        print(token)
        headers = {'Authorization': token}

        # 发起请求
        response = self.http.request(url=url, method=case.method, data=request_data, headers=headers)
        time.sleep(2)

        # 以下打印内容会显示在html测试报告中
        print()
        print('请求地址--> {}'.format(url))
        print('请求参数--> {}'.format(case.request_data))
        print('期望的测试结果--> {}'.format(case.expected_data))
        print('服务器响应数据--> {}'.format(response.json()))

        response_data = response.json()

        # 增加项目成功时 将服务器返回的数据中的id,create_time,update_time,is_delete 去掉 再来断言
        if response_data.get('id'):
            response_data.pop('id')
            response_data.pop('create_time')
            response_data.pop('update_time')
            response_data.pop('is_delete')

            expected_data = request_data
        else:
            expected_data = eval(case.expected_data)

        try:
            self.assertEqual(expected_data, response_data)
        except AssertionError as e:
            result = 'FAIL'
            output_log.exception(e)
            # 抛出异常 脚本才会将该条用例识别成测试失败
            raise e
        else:
            result = 'PASS'
            output_log.info('预期结果: {}, 实际结果: {}， 断言结果: {}'.format(case.expected_data, response_data, result))
        finally:
            # 向excel回写数据
            self.wb.write_data(row=self.row, column=10, value=str(response.json()))
            self.wb.write_data(row=self.row, column=11, value=result)


if __name__ == '__main__':
    env = conf.get('env', 'env')
    if env == 'all':
        run(CASE_DIR)
    elif env == 'one':
        # 命令行执行该测试脚本所有用例 test_add_project.py
        run('test_add_project')
    #111111
