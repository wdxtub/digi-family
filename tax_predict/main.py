import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet

# 需要按照 Prophet 要求的格式进行处理
df = pd.read_csv('data/tax_data.csv', usecols=[0, 1], engine='python')
df.ds = pd.to_datetime(df.ds)
print(df.head())
#print("将在弹出框显示图片，关闭图片后继续")
#plt.plot(df.y)
#plt.show()

print("创建 Prophet 对象")
# season 这里用来处理波动
changepoints = ['2015-01', '2015-04', '2015-05', '2015-07', '2015-10',
'2016-01', '2016-04', '2016-05', '2016-07', '2016-10',
'2017-01', '2017-04', '2017-05', '2017-07', '2017-10',
'2018-01', '2018-04', '2018-05',]
m = Prophet(yearly_seasonality=True, changepoints=changepoints)
m.fit(df)
future = m.make_future_dataframe(freq='M', periods=4)

forecast = m.predict(future)
m.plot(forecast)
plt.show()
print("Done")
