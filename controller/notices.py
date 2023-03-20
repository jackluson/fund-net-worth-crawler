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
    st_stocks = each_api_east_money.get_all_stocks_with_st()
    process_st_stocks = []
    for stock in st_stocks:
        stock_name = stock.get('f14')
        stock_code = stock.get('f12')
        process_st_stocks.append({
            **stock,
            'name': stock_name,
            'code': stock_code,
        })
    return process_st_stocks


pre_stocks = [
    {
        "code": '300705',
        "name": '九典制药'
    },
    {
        "code": '300986',
        "name": '志特新材'
    },
    {
        "code": '000498',
        "name": '山东路桥'
    },
    {
        "code": '300967',
        "name": '晓鸣股份'
    },
    {
        "code": '300740',
        "name": '水羊股份'
    },
    {
        "code": '300793',
        "name": '佳禾智能'
    },
    {
        "code": '300787',
        "name": '海能实业'
    },
    {
        "code": '300409',
        "name": '道氏技术'
    },
    {
        "code": '300452',
        "name": '山河药辅'
    },
    {
        "code": '300918',
        "name": '南山智尚'
    },
    {
        "code": '301046',
        "name": '能辉科技'
    },
    {
        "code": '603051',
        "name": '鹿山新材'
    },
    {
        "code": '000528',
        "name": '柳工'
    },
    {
        "code": '603228',
        "name": '景旺电子'
    },
    {
        "code": '300879',
        "name": '大叶股份'
    },
    {
        "code": '603180',
        "name": '金牌厨柜'
    },
    {
        "code": '002860',
        "name": '星帅尔'
    },
    {
        "code": '003036',
        "name": '泰坦股份'
    },
    {
        "code": '300480',
        "name": '光力科技'
    },
    {
        "code": '002120',
        "name": '韵达股份'
    },
]

position_stocks = [
    {
        "code": '002427',
        "name": '*ST尤夫'
    },
    {
        "code": '600654',
        "name": '*ST中安'
    },
    {
        "code": '600078',
        "name": 'ST澄星'
    },
    {
        "code": '600547',
        "name": '山东黄金'
    },
    {
        "code": '601233',
        "name": '桐昆股份'
    },
    {
        "code": '000063',
        "name": '中兴股份'
    },
    {
        "code": '600887',
        "name": '伊利股份'
    },
    {
        "code": '600031',
        "name": '三一重工'
    },
    {
        "code": '600585',
        "name": '海螺水泥'
    },
    {
        "code": '002624',
        "name": '完美世界'
    },
    {
        "code": '300326',
        "name": '凯利泰'
    },
    {
        "code": '603609',
        "name": '禾丰股份'
    },
    {
        "code": '600461',
        "name": '洪城环境'
    },
    {
        "code": '002157',
        "name": '正邦科技'
    },
    {
        "code": '603569',
        "name": '长久物流'
    },
    {
        "code": '600438',
        "name": '通威股份'
    },
    {
        "code": '002008',
        "name": '大族激光'
    }
]


def check_notices():
    # target_date_str = '2023-03-17'
    target_date_str = datetime.now().strftime("%Y-%m-%d")
    target_date = parser.parse(target_date_str)
    input_value = input("请输入下列序号执行操作:\n \
        1.“持有标的公告” \n \
        2.“预发转债标的公告” \n \
        3.“ST公告” \n \
    输入：")
    if input_value == '1':
        stocks = position_stocks
        file_dir = f'{os.getcwd()}/data/position_notices/'
        file_path = f'{file_dir}/{target_date_str}.xlsx'
        print(f"一共有{len(stocks)}只股票")
    elif input_value == '2':
        stocks = pre_stocks
        file_dir = f'{os.getcwd()}/data/pre_notices/'
        file_path = f'{file_dir}/{target_date_str}.xlsx'
        print(f"一共有{len(stocks)}只股票")
    elif input_value == '3':
        stocks = fetch_st_stocks()
        file_dir = f'{os.getcwd()}/data/st_notices/'
        file_path = f'{file_dir}/{target_date_str}.xlsx'
        print(f"一共有{len(stocks)}只ST股票")
    next_target_date = target_date + relativedelta(days=1)
    update_count = 0
    update_stocks = []
    is_after_target_day = True
    update_notices = []
    for stock in stocks:
        stock_name = stock.get('name')
        stock_code = stock.get('code')
        notice_list = fetch_notice_data(stock_code)
        news_count = 0
        for item in notice_list:
            notice_date = parser.parse(item['notice_date'])
            publish_date = parser.parse(item['eiTime'][0:19])
            if (is_after_target_day or next_target_date >= publish_date) and publish_date >= target_date:
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
    text = '之后' if is_after_target_day else '当天'
    print(f"{target_date_str}{text}(截至{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})共有{update_count}只ST股更新了{len(update_notices)}条公告")
    file_detail_data = pd.DataFrame(update_notices).rename(
        columns=detail_map).reset_index(drop=True)
    # print(file_detail_data)
    file_summary_data = pd.DataFrame(update_stocks).rename(
        columns=summay_map).reset_index(drop=True)
    update_xlsx_file(file_path, file_detail_data, '公告明细')
    update_xlsx_file(file_path, file_summary_data, '公告汇总')


if __name__ == '__main__':
    check_notices()
