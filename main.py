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
    code = "001043"
    month = '2021-07'
    handle_net_worth_data(code, month=month)
