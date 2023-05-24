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
from enum import Enum
from scripts.git import commit


class SourceType(Enum):
    POSITION = 1
    PRE = 2
    ST = 3


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
        "code": "688103",
        "name": "国力股份"
    },
    {
        "code": "300644",
        "name": "南京聚隆"
    },
    {
        'code': "301022",
        'name': "海泰科"
    },
    {
        'code': "301008",
        'name': "宏昌科技"
    },
    {
        'code': "300926",
        'name': "博俊科技"
    },
    {
        'code': '300829',
        'name': '金丹科技'
    },
    {
        "code": '300980',
        "name": '祥源新材'
    },
    {
        "code": '301098',
        "name": '金埔园林'
    },
    {
        "code": '300878',
        "name": '维康药业'
    },
    {
        "code": '300705',
        "name": '九典制药'
    },
    {
        "code": '300793',
        "name": '佳禾智能'
    },
    {
        "code": '300452',
        "name": '山河药辅'
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
]

position_stocks = [
    {
        "code": '128114',
        "name": '正邦转债'
    },
    {
        "code": '600241',
        "name": 'ST时万'
    },
    {
        "code": '002087',
        "name": 'ST新纺'
    },
    {
        "code": '000564',
        "name": 'ST大集'
    },
    {
        "code": '603133',
        "name": '*ST碳元'
    },
    {
        "code": '600543',
        "name": '*ST莫高'
    },
    {
        "code": '113640',
        "name": '苏利转债'
    },
    {
        "code": '110084',
        "name": '贵燃转债'
    },
    {
        "code": '113561',
        "name": '正裕转债'
    },
    {
        "code": '002717',
        "name": '岭南转债'
    },
    {
        "code": '113054',
        "name": '绿动转债'
    },
    {
        "code": '300793',
        "name": '佳禾智能'
    },
    {
        "code": '002083',
        "name": '孚日转债'
    },
    {
        "code": '601330',
        "name": '绿动转债'
    },
    {
        "code": '000895',
        "name": '双汇发展'
    },
    {
        "code": '603109',
        "name": '神驰机电'
    },
    {
        "code": '600382',
        "name": 'ST广珠'
    },
    {
        "code": '600078',
        "name": 'ST澄星'
    },
    {
        "code": '601233',
        "name": '桐昆股份'
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
        "code": '603007',
        "name": '花王转债'
    },
    {
        "code": '002203',
        "name": '海亮转债'
    }
]


class Notice():
    file_dir = None
    file_path = None
    update_stocks = []
    update_notices = []
    type: SourceType = None

    def __init__(self) -> None:
        target_date_str = datetime.now().strftime("%Y-%m-%d")
        self.target_date_str = target_date_str
        self.target_date = parser.parse(target_date_str)
        target_time_str = datetime.now().strftime('%H:%M:%S')
        self.target_time = target_time_str
        self.is_after_target_day = True
        self.suffix = f"(截至{target_time_str})" if target_time_str else ''
        self.api = ApiEastMoney()

    def set_stocks_source(self, type: SourceType = SourceType.POSITION):
        self.type = type
        if type == SourceType.POSITION:
            print('===========================持仓股票===========================')
            stocks = position_stocks
            self.file_dir = f'{os.getcwd()}/data/position_notices/'
            self.file_path = f'{self.file_dir}/{self.target_time}{self.suffix}.xlsx'
        elif type == SourceType.PRE:
            print('===========================配债股===========================')
            stocks = pre_stocks
            self.file_dir = f'{os.getcwd()}/data/pre_notices/'
            self.file_path = f'{self.file_dir}/{self.target_date_str}{self.suffix}.xlsx'
        elif type == SourceType.ST:
            print('===========================ST股===========================')
            stocks = fetch_st_stocks()
            self.file_dir = f'{os.getcwd()}/data/st_notices/'
            self.file_path = f'{self.file_dir}/{self.target_date_str}_ST股公告{self.suffix}.xlsx'
        print(f"一共有{len(stocks)}只股票")
        self.stocks = stocks

    def get_stocks_notice(self):
        next_target_date = self.target_date + relativedelta(days=1)
        update_stocks = []
        update_notices = []
        for stock in self.stocks:
            stock_name = stock.get('name')
            stock_code = stock.get('code')
            notice_list = fetch_notice_data(stock_code)
            news_count = 0
            for item in notice_list:
                notice_date = parser.parse(item['notice_date'])
                publish_date = parser.parse(item['eiTime'][0:19])
                if (self.is_after_target_day or next_target_date >= publish_date) and publish_date >= self.target_date:
                    print(stock_name, stock_code, item['title'])
                    news_count += 1
                    notice_detail = self.api.get_notice_detail(
                        art_code=item['art_code']).get('data')
                    update_notices.append({
                        'stock_name': stock_name,
                        'stock_code': stock_code,
                        'title': item['title'],
                        'notice_date': item['notice_date'],
                        'eiTime': item['eiTime'],
                        'attach_url': notice_detail['attach_url'],
                        # 'link': f"https://data.eastmoney.com/notices/detail/{stock_code}/{item['art_code']}.html",
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
        self.update_stocks = update_stocks
        self.update_notices = update_notices

    def output_excel(self):
        detail_map = {
            'stock_name': '股票名称',
            'stock_code': '股票代码',
            'title': '公告标题',
            'eiTime': '公告发布时间',
            'notice_date': '公告日期',
            'attach_url': '公告附件',
            # 'link': '公告链接',
        }
        summay_map = {
            'stock_name': '股票名称',
            'stock_code': '股票代码',
            'news_count': '公告数量'
        }
        text = '之后' if self.is_after_target_day else '当天'
        print(f"{self.target_date_str}{text}(截至{datetime.now().strftime('%Y-%m-%d %H:%M:%S')})共有{len(self.update_stocks)}只股更新了{len(self.update_notices)}条公告")
        if len(self.update_notices) == 0:
            return
        file_detail_data = pd.DataFrame(self.update_notices).rename(
            columns=detail_map).reset_index(drop=True)
        # print(file_detail_data)
        file_summary_data = pd.DataFrame(self.update_stocks).rename(
            columns=summay_map).reset_index(drop=True)
        update_xlsx_file(self.file_path, file_detail_data, '公告明细')
        update_xlsx_file(self.file_path, file_summary_data, '公告汇总')
        print('===========================输出完成===========================\n')

    def run(self, type: SourceType = SourceType.POSITION, *, after_run=False):
        self.set_stocks_source(type)
        self.get_stocks_notice()
        self.output_excel()
        if after_run:
            self.after_run()

    def run_all(self):
        self.run(SourceType.POSITION)
        self.run(SourceType.PRE)
        self.run(SourceType.ST)
        self.after_run()

    def after_run(self):
        if len(self.update_notices) == 0:
            return
        opt = input("是否commit当天数据:\n \
            1: 是. -- Y \n \
            2: 否. -- N \n \
        输入：")
        if opt == '1' or opt == "Y":
            commit()


def output_notice():
    notice = Notice()
    notice.run_all()


if __name__ == '__main__':
    output_notice()
