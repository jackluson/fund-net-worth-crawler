'''
Desc: 处理净值逻辑
File: /handle_net_worth.py
Project: controller
File Created: Saturday, 30th October 2021 6:36:43 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''
import time
import pandas as pd

from api.eastmoney import ApiEastMoney


def handle_net_worth_data():
    each_api_east_money = ApiEastMoney()
    code = "163402"
    start_date = '2020-08-01'
    end_date = '2020-08-30'
    # print(time.localtime(start_date))
    page_index = 1
    page_size = 30

    rsp = each_api_east_money.get_fund_net_worth(
        code=code,
        start_date=start_date,
        end_date=end_date,
        page_index=page_index,
        page_size=page_size,
    )
    print("rsp", rsp)
    net_list = rsp.get('Data').get('LSJZList')
    if len(net_list) == 0:
        print('当前参数没有净值数据')
        return
    pd_net_wortch_list = pd.DataFrame(net_list)
    pd_net_wortch_list.rename(columns={
                              'FSRQ': 'date', 'DWJZ': 'unit_net', 'LJJZ': 'accumulate_net', 'JZZZL': 'percent', 'FHSP': 'dividend'}, inplace=True)
    pd_net_wortch_list = pd_net_wortch_list[[
        'date', 'unit_net', 'accumulate_net', 'percent', 'dividend']]
    pd_net_wortch_list.set_index('date', inplace=True)


if __name__ == '__main__':
    handle_net_worth_data()
