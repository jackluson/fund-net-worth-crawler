'''
Desc: 入口文件
File: /main.py
Project: fund_net_worth
File Created: Saturday, 30th October 2021 6:40:59 pm
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''

from controller.backtesting import backtesting, backtesting_high_scores_fund
from controller.diviend_rate import diviend_rate
from controller.kline_trend import kline_trend
from controller.wglh import wglh
if __name__ == "__main__":
    # check_notices()
    # backtesting()
    # kline_trend()
    # exit()
    select = int(input("选选择执行哪项操作:\n \
        1: 双低查询 \n \
        2: 回测高分基金组合 \n \
        3: 双低趋势 \n \
    输入："))
    if select == 1:
        diviend_rate()
        # wglh.parse_html_script()
    elif select == 2:
        backtesting_high_scores_fund()
    elif select == 3:
        kline_trend()
