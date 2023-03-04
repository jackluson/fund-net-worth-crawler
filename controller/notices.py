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
from utils.file import write_fund_json_data, update_xlsx_file
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
    code = '600654'
    target_date_str = '2023-03-04'
    st_stocks = fetch_st_stocks()
    print("st_stocks", len(st_stocks))
    # target_date = datetime.now().strftime("%Y-%m-%d")
    target_date = parser.parse(target_date_str)
    update_count = 0
    update_stocks = []
    update_notices = []
    for stock in st_stocks:
        stock_name = stock.get('f14')
        stock_code = stock.get('f12')
        notice_list = fetch_notice_data(stock_code)
        news_count = 0
        for item in notice_list:
            notice_date = parser.parse(item['notice_date'])
            if notice_date >= target_date:
                # print('new')
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
                    'link': 'https://data.eastmoney.com/notices/detail/' + stock_code + item['art_code'] + '.html',
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
                # 'update_notices': 'update_notices'
            })
    print(f"共有{update_count}只ST股更新了公告")
    file_dir = f'{os.getcwd()}/data/ST公告/'

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
        print("目录新建成功：%s" % file_dir)
    # display_date = datetime.now().strftime("%Y-%m-%d")
    # lastest_data = fetch_notice_data(code)
    # print("lastest_data", lastest_data)
    file_path = f'{file_dir}/{target_date_str}.xlsx'
    # file_summary_path = f'{file_dir}/summary.xlsx'
    # df.rename(columns=rename_map).reset_index(drop=True)
    file_detail_data = pd.DataFrame(update_notices).reset_index(drop=True)
    file_summary_data = pd.DataFrame(update_stocks).reset_index(drop=True)
    update_xlsx_file(file_path, file_detail_data, '公告明细')
    update_xlsx_file(file_path, file_summary_data, '公告汇总')


if __name__ == '__main__':
    check_notices()
