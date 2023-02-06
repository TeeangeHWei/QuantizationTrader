'''
@desc 用来创建交易策略、生成交易信号
'''
import datetime
import data.Stock as st
import numpy as np
import matplotlib.pyplot as plt
def compose_signal(data):
    """
    整合信号
    :param data:
    :return:
    """
    data['buy_signal'] = np.where((data['weekday'] == 1)
                                  & (data['buy_signal'].shift(1) == 1), 0, data['buy_signal'])
    data['sell_signal'] = np.where((data['weekday'] == -1)
                                   & (data['sell_signal'].shift(1) == -1), 0, data['sell_signal'])
    data['signal'] = data['buy_signal'] + data['sell_signal']

    return data

def calculate_prof_pct(data):
    """
    # 计算单词收益率：开仓、平仓（开仓的全部股数）

    :param data:
    :return:
    """
    data = data[data['signal'] != 0]
    data['profit_pct'] = (data['close'] - data['close'].shift(1)) / data['close']
    data = data[data['signal'] == -1]
    return data

def week_period_stratrgy(code,time_freq,start_date,end_date):
    data = st.get_single_stock_price(code,time_freq,start_date,end_date)
    # 新建周期字段
    data['weekday'] = data.index.weekday
    # 周四买入
    data['buy_signal'] = np.where((data['weekday'] == 3),1,0)
    # 周一卖出

    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)

    # 整合信号
    data = compose_signal(data)
    # 计算收益率
    data = calculate_prof_pct(data)
    return data

if __name__ == '__main__':
    df = week_period_stratrgy('000001.XSHE','daily', None, datetime.date.today())
    print(df[['close','signal','profit_pct']])
    print(df.describe())
    df['profit_pct'].plot()
    plt.show()