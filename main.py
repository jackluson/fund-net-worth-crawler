'''
Desc: 入口文件
File: /main.py
Project: fund_net_worth
File Created: Saturday, 30th October 2021 6:40:59 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''

import pandas as pd
from controller.handle_net_worth import handle_net_worth_data


def backtesting_high_scores_fund():
    file_path = '/Users/admin/personal/anchor_plan/fund-morning-star-crawler/outcome/数据整理/funds/high-score-funds.xlsx'
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    print("xls.sheet_names", xls.sheet_names)
    year = '2021'
    practice_percent = 1
    quarter_map = {
        '2020-Q4': [2, 3, 4],
        '2021-Q1': [5, 6, 7],
        '2021-Q2': [8, 9, 10],
        '2021-Q3': [11, 12, 1],
    }
    for sheet_name in (xls.sheet_names):
        df_cur_sheet = xls.parse(sheet_name, converters={'代码': str})
        count = 5
        radio = 1 / count
        print("radio", radio)
        year_percent = 1
        month_list = quarter_map[sheet_name]
        for month in range(2, 12, 1):
            if month in month_list:
                av_percent = 0
                date = year + '-' + (str(month) if month >
                                     9 else '0' + str(month))
                for index, row in df_cur_sheet.iterrows():
                    # print("index", index)
                    # print('index', index, "row", row)
                    # if index >= 15 or index < 5:
                    if index >= count:
                        continue
                    code = row['代码']
                    name = row['名称']
                    period_percent = handle_net_worth_data(code, month=date)
                    print("code:{code},name:{name} date:{date}, percent:{percent}".format(
                        code=code,
                        name=name,
                        date=date,
                        percent=str(period_percent) + '%'
                    ))
                    av_percent += round(period_percent * radio, 4)
                    # print("code:{code},name:{name} date:{date}, percent:{percent}".format(
                    #     code=code,
                    #     name=name,
                    #     date=date,
                    #     percent=str(period_percent) + '%'
                    # ))
                # print('{sheet_name}组合{date}月份组合加权平均涨幅{percent}'.format(
                #     sheet_name=sheet_name,
                #     date=date,
                #     percent=str(round(av_percent, 4)) + '%'
                # ))
                year_percent = round((1 + av_percent/100)*year_percent, 4)
                practice_percent = round(
                    (1 + av_percent/100)*practice_percent, 4)
                print('{sheet_name}组合{date}月份组合加权平均涨幅{percent}'.format(
                    sheet_name=sheet_name,
                    date=date,
                    percent=str(round(av_percent, 4)) + '%'
                ))
                print("practice_percent", practice_percent)
        # print('{sheet_name}组合{year}年份加权平均涨幅{percent}'.format(
        #     sheet_name=sheet_name,
        #     year=year,
        #     percent=str(round((year_percent - 1) * 100, 4)) + '%'
        # ))
    print('practice_percent', practice_percent, 'count', count)


def backtesting_fund_portfolios_year():
    sheet_name = '2021-Q3'
    year = '2020'
    file_path = '/Users/admin/personal/anchor_plan/fund-morning-star-crawler/outcome/数据整理/funds/high-score-funds.xlsx'
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    # item_quarter_data = [sheet_name]
    df_cur_sheet = xls.parse(sheet_name, converters={'代码': str})
    # radio = round(1 / len(df_cur_sheet), 3)
    count = 5
    radio = 1 / count
    print("radio", radio)
    year_percent = 1
    # print("month_list", month_list)
    for month in range(1, 13):
        av_percent = 0
        date = year + '-' + (str(month) if month >
                             9 else '0' + str(month))
        for index, row in df_cur_sheet.iterrows():
            # print("index", index)
            # print('index', index, "row", row)
            # if index >= 15 or index < 5:
            if index >= count:
                continue
            code = row['代码']
            name = row['名称']
            period_percent = handle_net_worth_data(code, month=date)
            print("code:{code},name:{name} date:{date}, percent:{percent}".format(
                code=code,
                name=name,
                date=date,
                percent=str(period_percent) + '%'
            ))
            av_percent += round(period_percent * radio, 4)
        year_percent = round((1 + av_percent/100)*year_percent, 4)
        print('{sheet_name}组合{date}月份组合加权平均涨幅{percent}, 年化收益率{year_percent}'.format(
            sheet_name=sheet_name,
            date=date,
            percent=str(round(av_percent, 4)) + '%',
            year_percent=str(round(year_percent, 4)) + '%'
        ))


def backtesting_fund_portfolios_month():
    fund_list = [
        {
            'code': "001811",
            'radio': 0.2
        },
        {
            'code': '001054',
            'radio': 0.2
        },
        {
            'code': '000991',
            'radio': 0.1
        },
        {
            'code': '540003',
            'radio': 0.2
        },
        {
            'code': '163409',
            'radio': 0.2
        },
        {
            'code': '000547',
            'radio': 0.1
        }
    ]
    month = '2021-11'
    av_percent = 0
    for fund in fund_list:
        code = fund.get('code')
        radio = fund.get('radio')
        period_percent = handle_net_worth_data(code, month=month)
        av_percent += period_percent * radio
        print("code:{0}, date:{1}, precent:{2}".format(
            code, month, str(period_percent) + '%'))
    av_percent = round(av_percent, 4)
    print('{0}月份组合加权平均涨幅{1}'.format(month, str(av_percent) + '%'))


if __name__ == "__main__":
    # backtesting_high_scores_fund()
    # backtesting_fund_portfolios_year()
    backtesting_fund_portfolios_month()
