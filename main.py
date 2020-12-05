# -*- coding: utf-8 -*-



import unittest
import os
import time

from library.HTMLTestRunnerNew import HTMLTestRunner
from common.config import conf
from common.constant import CASE_DIR, REPORTS_DIR


def run(test_path):

    # 设置报告信息
    title = conf.get('report', 'title')
    description = conf.get('report', 'description')
    tester = conf.get('report', 'tester')
    report_name = conf.get('report', 'report_name')
    report_name = time.strftime("%Y%m%d%H%M%S", time.localtime()) + "_" + report_name
    report_path = os.path.join(REPORTS_DIR, report_name)

    # 创建测试集合
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    if os.path.isdir(test_path):
        suite.addTest(loader.discover(test_path))
    else:
        suite.addTest(loader.loadTestsFromName(test_path))

    with open(report_path, 'wb') as f:
        runner = HTMLTestRunner(
            # stream html文件对象
            stream=f,
            title=title,
            description=description,
            tester=tester
        )
        runner.run(suite)


if __name__ == '__main__':
    # 运行全部用例
    run(CASE_DIR)

