# -*- coding: utf-8 -*-
# 引入必要的库
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
from scipy import stats
import pylab
import seaborn
import pandas as pd
import datetime

# 数据文件地址
filename = "./presidential_polls.csv"

# 计算平均值函数
def get_avg(array):
    length = len(array)
    float_array = np.array(array, np.float64)
    return np.sum(array) / length

def main():
    df = pd.read_csv(filename)
    # 查看列名
    print df.columns
    # 使用的列名
    use_columns = ['enddate',
                   'rawpoll_clinton',
                   'rawpoll_trump',
                   'adjpoll_clinton',
                   'adjpoll_trump']

    # 获取相应的DataFrame
    df = df[use_columns]
    # 查看变量类别
    print df.dtypes

    # 处理日期格式数据
    enddates = df['enddate'].values.tolist()
    # 将日期字符串格式统一为 'YYYY/mm/dd'
    enddates = [enddate.replace("-", "/") for enddate in enddates]
    date_lst = [datetime.datetime.strptime(endtime, "%m/%d/%Y") for endtime in enddates]

    # 构造年份-月份列表
    month_lst = ['%d-%02d' % (date_obj.year, date_obj.month) for date_obj in date_lst]
    months = np.unique(month_lst)
    print type(months)
    print months

    # 清洗后的数据
    df['enddate'] = month_lst

    # 按月统计民调支持率
    results = pd.DataFrame(np.zeros((12,4)), index=months, columns=use_columns[1:])
    for month in months:
        # Hilary Clinton
        results.loc[month, "rawpoll_clinton"] = get_avg(df.loc[df['enddate'] == month, "rawpoll_clinton"])
        results.loc[month, "adjpoll_clinton"] = get_avg(df.loc[df['enddate'] == month, "adjpoll_clinton"])
        # Donald Trump
        results.loc[month, "rawpoll_trump"] = get_avg(df.loc[df['enddate'] == month, "rawpoll_trump"])
        results.loc[month, "adjpoll_trump"] = get_avg(df.loc[df['enddate'] == month, "adjpoll_trump"])

    # 原始民调走势图
    plt.plot(results['rawpoll_clinton'].values, label='Raw Poll Clinton')
    plt.plot(results['rawpoll_trump'].values, label='Raw Poll Trump')
    plt.xticks(range(12), months, rotation='vertical')
    plt.legend()
    plt.show()

    # 调整后民调走势图
    plt.plot(results['adjpoll_clinton'].values, label='Adj Poll Clinton')
    plt.plot(results['adjpoll_trump'].values, label='Adj Poll Trump')
    plt.xticks(range(12), months, rotation='vertical')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
