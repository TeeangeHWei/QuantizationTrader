import pandas as pd

import data.Stock as st
code = '000001.XSHE'
#调用一直股票行情数据
data = st.get_single_stock_price(code=code,
                                 time_freq='daily',
                                 start_date='2022-12-31',
                                 end_date='2023-1-31')

# 存入csv
st.export_data(data=data,filename=code,type='price')
# 从CSV中获取数据
data = st.get_csv_data(code=code,type='price')
print(data)

# 实时更新数据：假设每天更新日看数据

