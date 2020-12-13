# =================conding: utf-8
"""
================================================================================

Author : Administrator
Created  on : 2020/12/4

E-mail: zh13997821732@163.com


================================================================================

"""


import requests
from requests.sessions import Session

from common.logger import output_log


class HTTPRequest(object):
    """
    自动记录cookies信息给后续请求使用
    """

    def __init__(self):
        self.session = Session()

    def request(self, method, url, params=None, data=None, json=None, headers=None, cookies=None):
        method = method.lower()
        if method == 'get':
            output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 请求头: {}'.format(url, params, headers))
            return self.session.get(url=url, params=params, headers=headers, cookies=cookies)
        elif method == 'post':
            if data is not None:
                output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: form-data, 请求头: {}'.format(url, data, headers))
                return self.session.post(url=url, data=data, headers=headers, cookies=cookies)
            elif json is not None:
                output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: json, 请求头: {}'.format(url, json, headers))
                return self.session.post(url=url, json=json, headers=headers, cookies=cookies)
        elif method == 'put':
            output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: data, 请求头: {}'.format(url, data, headers))
            return self.session.put(url=url, data=data, headers=headers, cookies=cookies)
        elif method == 'delete':
            output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: data, 请求头: {}'.format(url, data, headers))
            return self.session.delete(url=url, data=data, headers=headers, cookies=cookies)

    def close(self):
        self.session.close()


class HTTPRequest2(object):

     def request(self, method, url, params=None, data=None, json=None, headers=None, cookies=None):
         method = method.lower()
         if method == 'get':
             output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}'.format(url, params))
             return requests.get(url=url, params=params, headers=headers, cookies=cookies)
         elif method == 'post':
             if data is not None:
                 output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: form-data'.format(url, data))
                 return requests.post(url=url, data=data, headers=headers, cookies=cookies)
             elif json is not None:
                 output_log.info('正在发送请求, 请求地址: {}, 请求参数: {}, 参数类型: json'.format(url, json))
                 return requests.post(url=url, json=json, headers=headers, cookies=cookies)











if __name__ == '__main__':

    # 原始的调用方法
    # response = requests.post(url=url, json=data, headers=None)

    http = HTTPRequest()

    url = 'http://42.192.88.224:8000/user/login/'
    data = {'username': 'aaaaaa', 'password': '11111'}
    response = http.request(url=url, method='post', json=data)
    print(response.json())
    # token = response.json().get('token')

    # url = 'http://42.192.88.224:8000/projects/names/'
    # headers = {'Authorization': token}
    # response = http.request(url=url, method='Get', headers=headers)
    # print(response.json())
