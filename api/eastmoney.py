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
import os
from .base import BaseApier
from utils.file import write_fund_json_data


class ApiEastMoney(BaseApier):
    def __init__(self):
        super().__init__()
        referer = 'http://fundf10.eastmoney.com/'
        self.referer = referer
        self.notice_api_base_url = 'https://np-anotice-stock.eastmoney.com/api'
        self.set_client_headers(cookie_env_key='eastmoney_')

    def get_fund_net_worth(self, *, code, start_date, end_date, page_index, page_size):
        timestamp = int(time.time() * 1000)
        callback = "jQuery18305757733125714872_" + str(timestamp)
        url = "http://api.fund.eastmoney.com/f10/lsjz?callback={callback}&fundCode={code}&pageIndex={page_index}&pageSize={page_size}&startDate={start_date}&endDate={end_date}&_={timestamp}".format(
            callback=callback,
            code=code,
            start_date=start_date,
            end_date=end_date,
            page_index=page_index,
            page_size=page_size,
            timestamp=timestamp
        )
        res = requests.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    def get_notices_info(self, *, code, page_size, page_index, ann_type):
        timestamp = int(time.time() * 1000)
        callback = "jQuery112308272385073717725_" + str(timestamp)
        url = "{base_url}/security/ann?cb={callback}&sr=-1&page_size={page_size}&page_index={page_index}&pageSize={page_size}&ann_type={ann_type}&client_source=web&stock_list={stock_list}&f_node={f_node}&s_node={s_node}".format(
            base_url=self.notice_api_base_url,
            callback=callback,
            page_size=page_size,
            page_index=page_index,
            ann_type=ann_type,
            stock_list=code,
            f_node=0,
            s_node=1,
        )
        res = requests.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    def get_notice_detail(self, *, art_code):
        timestamp = int(time.time() * 1000)
        callback = "jQuery11230024925577532673993_" + str(timestamp)
        url = "{base_url}/content/ann?cb={callback}&art_code={art_code}&page_index={page_index}&client_source=web&_{timestamp}".format(
            base_url="https://np-cnotice-stock.eastmoney.com/api",
            callback=callback,
            art_code=art_code,
            page_index=1,
            timestamp=timestamp,
        )
        res = requests.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-1]
                res_json = json.loads(data_text)
                return res_json
            else:
                print('请求异常', res)
        except:
            raise ('中断')

    def get_all_stocks_with_st(self, *, page_index=1, page_size=200):
        cur_date = time.strftime(
            "%Y-%m-%d", time.localtime(time.time()))
        file_dir = os.getcwd() + '/data/json/st/'
        filename = 'st_' + cur_date + '.json'
        is_exist = os.path.exists(file_dir + filename)
        if is_exist:
            with open(file_dir + filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        timestamp = int(time.time() * 1000)
        callback = "jQuery112405829056173474523_" + str(timestamp)

        url = "http://94.push2.eastmoney.com/api/qt/clist/get?cb={callback}&pn={page_index}&pz={page_size}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&wbp2u=|0|0|0|web&fid=f3&fs=b:BK0511+f:\u002150&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1677925812996".format(
            callback=callback,
            page_index=page_index,
            page_size=page_size,
        )
        res = requests.get(url, headers=self.headers)
        try:
            if res.status_code == 200:
                data_text = res.text.replace(callback, '')[1:-2]
                res_json = json.loads(data_text)
                write_fund_json_data(res_json.get(
                    'data').get('diff'), filename)
                return res_json.get('data').get('diff')
            else:
                print('请求异常', res)
        except:
            raise ('中断')
