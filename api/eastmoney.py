'''
Desc: 天天基金数据
File: /eastmoney.py
Project: api
File Created: Saturday, 30th October 2021 6:21:25 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''

import time
import json
import requests

from .base import BaseApier


class ApiEastMoney(BaseApier):
    def __init__(self):
        super().__init__()

    def get_fund_net_worth(self, *, code, start_date, end_date, page_index, page_size):
        timestamp = int(time.time() * 1000)
        callback = "jQuery18306767772725117951_" + str(timestamp)
        url = "http://api.fund.eastmoney.com/f10/lsjz?callback={callback}&fundCode={code}&pageIndex={page_index}&pageSize={page_size}&startDate={start_date}&endDate={end_date}&_={timestamp}".format(
            callback=callback,
            code=code,
            start_date=start_date,
            end_date=end_date,
            page_index=page_index,
            page_size=page_size,
            timestamp=timestamp
        )
        headers = self.get_client_headers()
        res = requests.get(url, headers=headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise('中断')
