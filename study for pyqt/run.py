# coding=utf-8

import pandas as pd

file_path = '/Users/yewen/Desktop/study for pyqt/mstp.xls'
raw_data = pd.read_excel(file_path, header=0, sheet_name='switch')
data = raw_data.values

##添加switch 信息
# 初始化switch 信息
switch_list = list()
print('-----switch信息添加----')
print(data)

