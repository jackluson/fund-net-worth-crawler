'''
Desc: 入口文件
File: /main.py
Project: fund_net_worth
File Created: Saturday, 30th October 2021 6:40:59 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''

from controller.handle_net_worth import handle_net_worth_data

if __name__ == "__main__":
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
    month = '2021-10'
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
