# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
#     問題設定:
# 

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# %%
# 期間
# steps日の株価変動を評価する
day_per_month = 20
steps = 36*day_per_month

# 月々の収入
# 毎月全額株を購入
monthly_income = 300000
# 月々の支出
monthly_outgo = 300000

# 保有株数
num_of_stock = 60

# 現金
# 月々の支出はここから捻出
# cash_base以下になったら、cash_targetになるよう株を一部換金
cash_current = 1500000
cash_target = 3600000
cash_base = 600000


# %%
# sample_number個の時系列データを生成し、株価の評価をする
sample_number = 100000


# %%
# 株価の日次時系列データ
pd_data = pd.read_csv('sample_data.csv',header=None)
raw_data= np.array(pd_data[0])

log_data = np.log(raw_data)
# 日次収益率
sample_rate= log_data[1:len(log_data)]-log_data[0:len(log_data)-1]


# %%
price = np.ones(sample_number)*raw_data[len(raw_data)-1]
n = np.ones(sample_number)*num_of_stock
# 株評価額
x = n * price

# sample_number個の株価データの平均値
x_avg = [x[0]]
# sample_number個の株価データの中間値
x_half = [x[0]]
# Value At Risk - 99%の確率で、株価はこれより高くなる
x_var = [x[0]]
# Average + 1 sigma相当 - 35%の確率で、株価はこれより高くなる
x_p = [x[0]]
# Average - 1 sigma相当 - 65%の確率で、株価はこれより高くなる
x_n = [x[0]]

# 全資産
total_avg = [x[0] + cash_current]
total_half = [x[0] + cash_current]
total_var = [x[0] + cash_current]
total_p = [x[0] + cash_current]
total_n = [x[0] + cash_current]

for i in range(1,steps+1):
    # 変動率をサンプリング
    index = np.random.randint(0,len(sample_rate),sample_number)
    price = (1+sample_rate[index])*price
    # 株評価額
    x = n * price

    # 毎月の収入と支出
    if i % day_per_month == 0:
        # 月々の収入 - 全額株を購入
        x = x + monthly_income
        n = x/price
        # 月々の支出 - 現金から捻出
        cash_current = cash_current - monthly_outgo
        # 現金が減ってきたので株を一部換金
        if cash_current <= cash_base:
            x = x - (cash_target - cash_current)
            n = x/price
            cash_current = cash_target

    x.sort()
    # sample_number個の株価データの平均値
    x_avg.append(np.average(x))
    # sample_number個の株価データの中間値
    x_half.append(x[int(0.5*sample_number)])
    # Value At Risk - 99%の確率で、株価はこれより高くなる
    x_var.append(x[int(0.01*sample_number)])
    # Average + 1 sigma相当 - 35%の確率で、株価はこれより高くなる
    x_n.append(x[int(0.35*sample_number)])
    # Average - 1 sigma相当 - 65%の確率で、株価はこれより高くなる
    x_p.append(x[int(0.65*sample_number)])

    # 全資産
    total_avg.append(np.average(x) + cash_current)
    total_half.append(x[int(0.5*sample_number)] + cash_current)
    total_var.append(x[int(0.01*sample_number)] + cash_current)
    total_n.append(x[int(0.35*sample_number)] + cash_current)
    total_p.append(x[int(0.65*sample_number)] + cash_current)

# %%
plt.plot(x_avg , label="Average")
plt.plot(x_half , label= "Half")
plt.plot(x_var , label= "Value At Risk")
plt.plot(x_p , label="+1 sigma")
plt.plot(x_n , label="-1 Sigma")
plt.legend()
plt.show()

# %%
plt.plot(total_avg , label="Average")
plt.plot(total_half , label= "Half")
plt.plot(total_var , label= "Value At Risk")
plt.plot(total_p , label="+1 sigma")
plt.plot(total_n , label="-1 Sigma")
plt.legend()
plt.show()
