import pandas as pd
from controller.handle_net_worth import handle_net_worth_data


def backtesting_high_scores_fund():
    """
    高分系列基金季度轮动回测
    """
    file_path = '/Users/admin/personal/anchor_plan/fund-morning-star-crawler/outcome/数据整理/funds/high-score-funds.xlsx'
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    print("xls.sheet_names", xls.sheet_names)
    practice_percent = 1
    quarter_map = {
        '2020-Q4': [2, 3, 4],
        '2021-Q1': [5, 6, 7],
        '2021-Q2': [8, 9, 10],
        '2021-Q3': [11, 12, 1],
        '2021-Q4': [2, 3, 4],
        '2022-Q1': [5, 6, 7],
        '2022-Q2': [8, 9, 10],
        '2022-Q3': [11, 12, 1],
    }
    # for sheet_name in (xls.sheet_names):
    for sheet_name in quarter_map.keys():
        df_cur_sheet = xls.parse(sheet_name, converters={'代码': str})
        count = 5
        radio = 1 / count
        year_percent = 1
        if not sheet_name in quarter_map:
            continue
        month_list = quarter_map[sheet_name]
        for month in month_list:
            av_percent = 0
            cur_year = sheet_name.split('-')[0]
            quarter_index = sheet_name.split('-')[1]
            if quarter_index == 'Q4':
                cur_year = str(int(cur_year) + 1)
            if quarter_index == 'Q3' and month == 1:
                cur_year = str(int(cur_year) + 1)
            date = cur_year + '-' + (str(month) if month >
                                     9 else '0' + str(month))
            memo_row = []
            for index, row in df_cur_sheet.iterrows():
                # print('index', index, "row", row)
                # if index >= 15 or index < 5:
                if len(memo_row) >= count:
                    continue
                code = row['代码']
                name = row['名称']
                manager = row['基金经理']
                if manager in memo_row:
                    continue
                memo_row.append(manager)
                period_percent = handle_net_worth_data(code, month=date)
                print("code:{code},name:{name} date:{date}, percent:{percent}".format(
                    code=code,
                    name=name,
                    date=date,
                    percent=str(period_percent) + '%'
                ))
                av_percent += round(period_percent * radio, 4)
            year_percent = round((1 + av_percent/100)*year_percent, 4)
            practice_percent = round(
                (1 + av_percent/100)*practice_percent, 4)
            print('{sheet_name}组合-{date}月份组合加权平均涨幅{percent}'.format(
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
    """
    某个季度高分系列基金前几名基金年化回撤
    """
    sheet_name = '2021-Q3'
    year = '2020'
    file_path = '/Users/admin/personal/anchor_plan/fund-morning-star-crawler/outcome/数据整理/funds/high-score-funds.xlsx'
    xls = pd.ExcelFile(file_path, engine='openpyxl')
    df_cur_sheet = xls.parse(sheet_name, converters={'代码': str})
    # radio = round(1 / len(df_cur_sheet), 3)
    count = 5
    radio = 1 / count
    year_percent = 1
    for month in range(1, 13):
        av_percent = 0
        date = year + '-' + (str(month) if month >
                             9 else '0' + str(month))
        for index, row in df_cur_sheet.iterrows():
            # print("index", index)
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


def backtesting_fund_portfolios_month(fund_list, month):
    av_percent = 0
    for fund in fund_list:
        code = fund.get('code')
        radio = fund.get('radio')
        # date = {
        #     'start_date': '2021-12-01',
        #     'end_date': '2021-12-22',
        # }
        period_percent = handle_net_worth_data(
            code, month=month, dimension='unit_net')
        fund['percent'] = str(period_percent) + '%'
        av_percent += period_percent * radio
        # print("code:{0}, date:{1}, precent:{2}".format(
        #     code, month, str(period_percent) + '%'))
    av_percent = round(av_percent, 2)
    df_fund_list = pd.DataFrame(
        fund_list, columns=["name", "code", "percent", "radio"])
    df_fund_list['radio'] = (df_fund_list['radio'] * 100).astype(str) + '%'
    df_fund_list.sort_values(by='percent', inplace=True,
                             ascending=False, ignore_index=True)
    df_fund_list.rename(columns={
        "name": "基金名称",
        "code": "基金代码",
        "percent": "基金涨幅",
        "radio": "组合占比",
    }, inplace=True)
    df_fund_list.set_index('基金名称', inplace=True)
    # print(df_fund_list)
    print(df_fund_list.to_markdown())
    print('{0}月份组合加权平均涨幅{1}'.format(month, str(av_percent) + '%'))


def backtesting():
    fund_group_history_list = [
        [
            {
                'code': "001811",
                'name': '中欧明睿新常态混合A',
                'radio': 0.2,
            },
            {
                'code': '001054',
                'name': '工银新金融股票A',
                'radio': 0.2
            },
            {
                'code': '000991',
                'name': '工银战略转型股票A',
                'radio': 0.1
            },
            {
                'code': '540003',
                'name': '汇丰晋信动态策略混合A',
                'radio': 0.2
            },
            {
                'code': '163409',
                'name': '兴全绿色投资混合(LOF)',
                'radio': 0.2
            },
            {
                'code': '000547',
                'name': '建信健康民生混合',
                'radio': 0.1
            }
        ],
        [
            {
                'code': '519002',
                'name': '华安安信消费混合',
                'radio': 0.2
            },
            {
                'code': '001718',
                'name': '工银瑞信物流产业股票',
                'radio': 0.2
            },
            {
                'code': '000991',
                'name': '工银瑞信战略转型主题股票A',
                'radio': 0.1
            },
            {
                'code': '540003',
                'name': '汇丰晋信动态策略混合A',
                'radio': 0.1
            },
            {
                'code': '450001',
                'name': '国富中国收益混合',
                'radio': 0.1
            },
            {
                'code': '000547',
                'name': '建信健康民生混合',
                'radio': 0.1
            },
            {
                'code': '163409',
                'name': '兴全绿色投资混合(LOF)',
                'radio': 0.2
            },
        ]
    ]
    fund_list_other = [
        {
            'code': "519002",
            'radio': 0.2,
            'name': '华安安信消费混合'
        },
        {
            'code': "163807",
            'name': '中银优选混合',
            'radio': 0.2
        },
        {
            'code': "000547",
            'name': '建信健康民生混合',
            'radio': 0.2
        },
        {
            'code': "001054",
            'name': '工银新金融股票',
            'radio': 0.2
        },
        {
            'code': "001694",
            'name': '华安沪港深外延增长灵活配置混合',
            'radio': 0.2
        }
    ]
    month = '2022-01'
    backtesting_fund_portfolios_month(fund_group_history_list[1], month)


if __name__ == "__main__":
    backtesting_high_scores_fund()
