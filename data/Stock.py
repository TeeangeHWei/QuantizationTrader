'''resample 函数的使用'''
import pandas as pd
from jqdatasdk import *
import datetime


pd.set_option('display.max_rows',10000)
pd.set_option('display.max_columns',1000)
auth('18824736811','Core1995')
root = '/Users/cyrus.h/Desktop/DebaoTrader/data/'

def get_stock_list():
    """
    获取所有A股股票列表
    :return: stock_list
    """
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

def get_single_stock_price(code,time_freq,start_date,end_date):
    """
    获取单个股票行情数据
    :param code:
    :param time_freq:
    :param start_date:
    :param end_date:
    :return:data
    """
    # 如果 start_date-none，默认为从上市日期开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    # 获取行情数据
    data = get_price(code,start_date=start_date,end_date=end_date,frequency=time_freq,panel=False)
    return data

def export_data(data,filename,type):
    """
    导出股票行情数据
    :param data:
    :param filename:
    :return:
    """
    file_root = root +type+'/' +filename+'.csv'
    data.index.names = ['date']
    data.to_csv(file_root)
    print('已成功存储至：',file_root)

def get_csv_data(code,type):
    file_root = root + type + '/' + code + '.csv'
    print('已成功读取：', file_root)
    return pd.read_csv(file_root)

def transfer_price_freq(data,time_freq):
    """
    将数据转换为指定周期 获取周K（当周的）：开盘价（当周第一天）、收盘价（当周最后一天）、最高价（当周）、最低价（当周）
    转换股票行情周期
    :param data:
    :param time_freq:
    :return: df_trans
    """

    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    return df_trans


def get_single_finance(code,date,statDate):
    """
    获取单个股票财务指标
    :param code:
    :param date:
    :param statDate:
    :return: data
    """
    data = get_fundamentals(query(indicator).filter(indicator.code == code ), date=date,statDate=statDate)
    return data



def get_single_valuation(code,date,statDate):
    """
    获取单个股票估值指标
    :param code:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == code), date=date, statDate=statDate)
    return data

def calculate_change_pct(data):
    """
    涨跌幅 = （当期收盘价-前期收盘价） /前期收盘价
    :param data: dataframe 带有收盘价
    :return: dataframe 带有涨跌幅
    """
    data['close_pct'] = (data['close'] - data['close'].shift(1))\
                        / data['close'].shift(1)

    return data

