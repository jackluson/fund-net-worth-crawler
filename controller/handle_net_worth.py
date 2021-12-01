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
    end_date_str = end_date.format('YYYY-MM-DD')
    start_date_str = start_date.format('YYYY-MM-DD')
    page_index = 1
    page_size = 30
    rsp = each_api_east_money.get_fund_net_worth(
        code=code,
        start_date=start_date_str,
        end_date=end_date_str,
        page_index=page_index,
        page_size=page_size,
    )
    return rsp


def handle_net_worch_month_data(code, month):
    """暂时没有考虑分红,拆分情况导致净值异常情况
    """
    start_date = arrow.get(month)
    start_date = start_date.shift(days=-1)
    end_date = start_date.dehumanize("in a month")
    rsp = fetch_net_data(code, start_date, end_date)
    pd_net_wortch_list = process_rsp_data(rsp)
    if pd_net_wortch_list.empty:
        return
    end_date_net = pd_net_wortch_list.head(
        1).iat[0, 0]
    if start_date.format('YYYY-MM-DD') in pd_net_wortch_list.index:  # 判断是否开始时间是否在当前数据内
        start_date_net = pd_net_wortch_list.tail(1).iat[0, 0]
    else:
        '''
        找不到上个月最后一天,则重新查询上个月所有交易日净值,取最后时间
        '''
        # 先求上一个月最后一天净值
        start_date = arrow.get(month).dehumanize("a month ago")  # 从前一天计算
        end_date = start_date.dehumanize("in a month").shift(days=-1)
        rsp = fetch_net_data(code, start_date, end_date)
        pd_net_wortch_list = process_rsp_data(rsp)
        if pd_net_wortch_list.empty:
            return
        start_date_net = pd_net_wortch_list.head(1).iat[0, 0]
    diff_net = round(end_date_net - start_date_net, 4)
    period_percent = round(diff_net / start_date_net * 100, 2)
    return period_percent


def handle_net_worth_data(code, *, month: date = None):
    if month:
        return handle_net_worch_month_data(code, month)
    else:
        print('目前只支持查询某个月份净值涨幅')


if __name__ == '__main__':
    handle_net_worth_data()
