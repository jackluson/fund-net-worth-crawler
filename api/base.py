'''
Desc: 基础类
File: /base.py
Project: api
File Created: Saturday, 30th October 2021 6:48:33 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''


class BaseApier:
    # def __init__(self):
    #     load_dotenv()

    def get_client_headers(self):
        # cookie = self.__dict__.get(cookie_env_key)
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36',
            'Origin': 'http://fundf10.eastmoney.com/',
            'Referer': 'http://fundf10.eastmoney.com/',
            # 'Cookie': cookie
        }
        return headers
