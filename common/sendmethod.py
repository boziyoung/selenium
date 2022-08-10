import requests
import json


class SendMethod:
    def __init__(self, method, url):
        self.method = method
        self.url = url

    def send_method(self, **kwargs):
        if self.method.lower() == 'get' or 'delete':
            response = requests.request(method=self.method, url=self.url, **kwargs)
        elif self.method.lower() == 'post' or 'put':
            response = requests.request(method=self.method, url=self.url, **kwargs)
        else:
            print('请求方式错误')
            response = None

        # 对请求的结果进行操作
        if self.method == 'delete':
            return response.status_code
        else:
            print(f'状态码：{response.status_code}')
            # time.sleep(2)
            # bs = BeautifulSoup(response.text, 'html.parser')
            return response
