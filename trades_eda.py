import pandas as pd
from datetime import datetime as dt
import matplotlib.pyplot as plt

df = pd.read_csv('djt_trades.csv')

df['time_dt'] = [dt.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ") for date in df['created_time']]
df['t'] = df['time_dt'] - dt(2024, 10, 4)
df['t'] = [delta.total_seconds() for delta in df['t']]
df = df.sort_values(by='t', ascending=True).reset_index(drop=True)
df['x'] = [min(df['t'])] + [df['t'][i] - df['t'][i-1] for i in range(1, len(df['t']))]
df = df[df["time_dt"] <= dt(2024, 11, 6, 9, 34)]

time_range = [dt(2024, 11, 6), dt(2024, 11, 6, 7)]
df_filt = df[(df["time_dt"] >= time_range[0]) & (df["time_dt"] <= time_range[1])]

plt.scatter(df_filt['t'], df_filt['yes_price'], s = 0.01)
plt.xlabel('Time (s)')
plt.ylabel('Price of Yes Contract (cents)')
plt.title('Price of Yes Position for Each Transation During Ballot Counting')

plt.scatter(df['x'][0:-1], df['x'][1:], s = 0.1, c = 'blue')
plt.xlim(0, 1000)
plt.ylim(0, 1000)
plt.xlabel('Wait time at time t (s)')
plt.ylabel('Wait time at time t+1 (s)')
plt.title('Wait Time Between Trades at t vs t+1')

plt.hist(df['x'])
plt.xlim(0, 1000)