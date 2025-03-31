import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import acf
import seaborn as sns
import scipy.stats as stats
import numpy as np
from statsmodels.tsa.stattools import kpss

def kpss_test(timeseries):
    print("Results of KPSS Test:")
    kpsstest = kpss(timeseries, regression="c", nlags="auto")
    kpss_output = pd.Series(
        kpsstest[0:3], index=["Test Statistic", "p-value", "Lags Used"]
    )
    for key, value in kpsstest[3].items():
        kpss_output["Critical Value (%s)" % key] = value
    print(kpss_output)

df = pd.read_csv('djt_trades.csv')

df['time_dt'] = [dt.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in df['created_time']]
df['t'] = df['time_dt'] - dt(2024, 10, 4)
df['t'] = [delta.total_seconds() for delta in df['t']]
df = df.sort_values(by='t', ascending=True).reset_index(drop=True)
df['x'] = [min(df['t'])] + [df['t'][i] - df['t'][i-1] for i in range(1, len(df['t']))]
df = df[df["time_dt"] <= dt(2024, 11, 6, 9, 34)]

time_range = [dt(2024, 11, 6), dt(2024, 11, 6, 7)]
time_len_s = int((time_range[1] - time_range[0]).total_seconds())
df_filt = df[(df["time_dt"] >= time_range[0]) & (df["time_dt"] <= time_range[1])].copy()
df_filt['t'] = df_filt['t'] - (time_range[0] - dt(2024, 10, 4)).total_seconds()
df_filt['t_ms'] = round(df_filt['t']*1000)

## Price Time Series

plt.scatter(df_filt['t'], df_filt['yes_price'], s = 0.01)
plt.xlabel('Time (s)')
plt.ylabel('Price of Yes Contract (cents)')
plt.title('Price of Yes Position for Each Transation During Ballot Counting')
plt.show()

# Wait time histogram

plt.hist(df_filt['x'], bins = 100)
plt.ylabel('Frequency')
plt.xlabel('Wait times (s)')
plt.title('Wait Times Between Trades During Ballot Counting')
plt.show()

# Wait time ACF

plot_acf(df_filt['x'], lags=30, bartlett_confint=True, zero=False)
acf_x = acf(df_filt['x'], nlags = 1000)

# Increment ACF

inc_m = np.histogram(df_filt['t']/60, bins = int(time_len_s/60), range=(0, time_len_s/60))[0]
inc_m_centered = inc_m - np.mean(inc_m)

plot_acf(inc_m_centered, lags = 30, zero = True)

plt.plot(range(0, 420), inc_m) 
plt.title('Increments of Process (binned in min)')

inc_m_diff = np.diff(inc_m)

plt.plot(range(1, 420), inc_m_diff) 
plt.title('Differenced Increments of Process (binned in min)')

plot_acf(inc_m_diff, lags = 30, title = 'ACF of Differenced Increments (min)')

# Same thing for secs

inc_s = np.histogram(df_filt['t'], bins = int(time_len_s), range=(0, time_len_s))[0]

inc_s_diff = np.diff(inc_s)

plt.plot(range(1, time_len_s), inc_s_diff) 
plt.title('Differenced Increments of Process (binned in sec)')

plot_acf(inc_s_diff, lags = 30, title = 'ACF of Differenced Increments (sec)')

kpss_test(inc_m_diff)
kpss_test(inc_s_diff)

# Exponential QQ plot of Wait Times

fig = plt.figure()
ax = fig.add_subplot(111)
stats.probplot(df_filt['x'], sparams=(0, np.mean(df_filt['x'])), dist='expon', plot=ax)

plt.setp(ax.lines[0], markersize=2)
plt.title('Exp QQ Plot for Wait Times During Ballot Counting')
plt.show()

# Scatterplot of all variables

sns.pairplot(df_filt[['x', 'count', 'yes_price']], )
plt.show()
