'''
Desc: 处理净值逻辑
File: /handle_net_worth.py
Project: controller
File Created: Saturday, 30th October 2021 6:36:43 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''
from datetime import date
import arrow
import numpy as np
import pandas as pd

from api.eastmoney import ApiEastMoney


def process_rsp_data(rsp):
    net_list = rsp.get('Data').get('LSJZList')
    if len(net_list) == 0:
        print('当前参数没有净值数据')
    pd_net_wortch_list = pd.DataFrame(net_list, dtype=np.float)
    if pd_net_wortch_list.empty:
        return pd_net_wortch_list
    pd_net_wortch_list.rename(columns={
                              'FSRQ': 'date', 'DWJZ': 'unit_net', 'LJJZ': 'accumulate_net', 'JZZZL': 'percent', 'FHSP': 'dividend'}, inplace=True)
    pd_net_wortch_list = pd_net_wortch_list[[
        'date', 'unit_net', 'accumulate_net', 'percent', 'dividend']]
    pd_net_wortch_list.set_index('date', inplace=True)
    return pd_net_wortch_list


def fetch_net_data(code, start_date, end_date):
    each_api_east_money = ApiEastMoney()
    # nd_date_str = end_date.format('YYYY-MM-DD')
    # start_date_str = start_date.format('YYYY-MM-DD')e
    page_index = 1
    page_size = 30
    rsp = each_api_east_money.get_fund_net_worth(
        code=code,
        start_date=start_date,
        end_date=end_date,
        page_index=page_index,
        page_size=page_size,
    )
    return rsp


def process_date_cur(date):
    if type(date) is str:
        start_date = arrow.get(date)
        # start_date = start_date.shift(days=-1)
        end_date = start_date.dehumanize(
            "in a month").shift(days=-1)  # 当前月最后一天
        return {
            'start_date': start_date.format('YYYY-MM-DD'),
            'end_date': end_date.format('YYYY-MM-DD')
        }


def handle_net_worth_month_data(code, *, month=None, date_dict):
    if month:
        date_dict = process_date_cur(month)
    print("date_dict", date_dict, date_dict.get('start_date'))
    """暂时没有考虑分红,拆分情况导致净值异常情况
    """
    start_date = date_dict.get('start_date')
    end_date = date_dict.get('end_date')
    # exit()
    rsp = fetch_net_data(code, start_date, end_date)
    pd_net_wortch_list = process_rsp_data(rsp)
    dimension = 'accumulate_net'  # unit_net
    if pd_net_wortch_list.empty:
        print(code, 'start_date', start_date, start_date)
        return
    end_date_net = pd_net_wortch_list.loc[pd_net_wortch_list.index[0]][dimension]

    # if start_date in pd_net_wortch_list.index:  # 判断是否开始时间是否在当前数据内
    start_date_pecent = pd_net_wortch_list.loc[pd_net_wortch_list.index[-1]
                                               ]['percent'] / 100
    last_start_date_net = round(pd_net_wortch_list.loc[pd_net_wortch_list.index[-1]][dimension] / (
        1+start_date_pecent), 4)

    diff_net = round(end_date_net - last_start_date_net, 4)
    period_percent = round(diff_net / last_start_date_net * 100, 2)
    return period_percent


def handle_net_worth_data(code, *, month=None, date=None):
    if month:
        return handle_net_worth_month_data(code, month=month)
    if date:
        return handle_net_worth_month_data(code, date_dict=date)
    else:
        print('目前只支持查询某个月份净值涨幅')


if __name__ == '__main__':
    handle_net_worth_data()
