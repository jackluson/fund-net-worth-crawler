'''
Desc:
File: /notices.py
File Created: Saturday, 4th March 2023 5:47:54 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2022 Camel Lu
'''
from api.eastmoney import ApiEastMoney
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import *
from utils.file import update_xlsx_file
import pandas as pd
import os


def fetch_notice_data(code):
    each_api_east_money = ApiEastMoney()
    rsp = each_api_east_money.get_notices_info(
        code=code,
        page_size=50,
        page_index=1,
        ann_type='A',
    )
    return rsp.get('data').get('list')


def fetch_st_stocks():
    each_api_east_money = ApiEastMoney()
    return each_api_east_money.get_all_stocks_with_st()


def check_notices():
    # target_date_str = '2023-03-08'
    st_stocks = fetch_st_stocks()
    print(f"一共有{len(st_stocks)}只ST股票")
    target_date_str = datetime.now().strftime("%Y-%m-%d")
    target_date = parser.parse(target_date_str)
    next_target_date = target_date + relativedelta(days=1)
    update_count = 0
    update_stocks = []
    is_after_current_day = False
    update_notices = []
    for stock in st_stocks:
        stock_name = stock.get('f14')
        stock_code = stock.get('f12')
        notice_list = fetch_notice_data(stock_code)
        news_count = 0
        for item in notice_list:
            notice_date = parser.parse(item['notice_date'])
            publish_date = parser.parse(item['eiTime'][0:-4])
            if (is_after_current_day or next_target_date >= publish_date) and publish_date >= target_date:
                print(stock_name, stock_code, item['title'])
                if news_count == 0:
                    update_count += 1
                news_count += 1
                update_notices.append({
                    'stock_name': stock_name,
                    'stock_code': stock_code,
                    'title': item['title'],
                    'notice_date': item['notice_date'],
                    'eiTime': item['eiTime'],
                    'link': f"https://data.eastmoney.com/notices/detail/{stock_code}/{item['art_code']}.html",
                })
                # if news_count > 2:
                #     break
            else:
                break
        if news_count > 0:
            update_stocks.append({
                'stock_name': stock_name,
                'stock_code': stock_code,
                'news_count': news_count,
            })
    file_dir = f'{os.getcwd()}/data/ST公告/'
    file_path = f'{file_dir}/{target_date_str}.xlsx'
    # file_summary_path = f'{file_dir}/summary.xlsx'
    detail_map = {
        'stock_name': '股票名称',
        'stock_code': '股票代码',
        'title': '公告标题',
        'eiTime': '公告发布时间',
        'notice_date': '公告日期',
        'link': '公告链接',
    }
    summay_map = {
        'stock_name': '股票名称',
        'stock_code': '股票代码',
        'news_count': '公告数量'
    }
    print(f"{target_date_str}当天(截至{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})共有{update_count}只ST股更新了{len(update_notices)}条公告")
    file_detail_data = pd.DataFrame(update_notices).rename(
        columns=detail_map).reset_index(drop=True)
    # print(file_detail_data)
    file_summary_data = pd.DataFrame(update_stocks).rename(
        columns=summay_map).reset_index(drop=True)
    update_xlsx_file(file_path, file_detail_data, '公告明细')
    update_xlsx_file(file_path, file_summary_data, '公告汇总')


if __name__ == '__main__':
    check_notices()
