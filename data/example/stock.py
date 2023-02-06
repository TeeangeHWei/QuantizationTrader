'''
desc:获取价格，并且计算涨跌幅
'''

import data.Stock as st

# 获取平安银行的行情数据（日K）
data = st.get_single_stock_price('000001.XSHE','daily','2022-12-31','2023-1-31')
# print(data)
# 计算涨跌幅，验证准确性
st.calculate_change_pct(data)
# 获取周K
data = st.transfer_price_freq(data,'W')
print(data)
#计算涨跌幅，验证准确性
data = st.calculate_change_pct(data)
print(data)
