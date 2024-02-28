import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.ticker import ScalarFormatter

def init():
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.set_xlabel('LOB level', color = 'white')
    ax.set_ylabel('Price' , color = 'white')
    ax.set_title('')
    ax.set_xticks(range(len(xlim)))
    ax.set_xticklabels(xlim)
    ax.set_ylim(inf_y, sup_y)
    ax.grid(False)

    bars = ax.bar(range(levels * 2), np.zeros(levels * 2), color='white')

    text_time = ax.text(5, sup_y, '', fontsize=12, ha='center', va='center', color='white')
    return bars, text_time

def update(frame, bars, text_time):
    text_time.set_text('')

    text_time.set_text(f'Time: {data.index[frame] / 1e9} sec')

    asks, bids = [], []
    for i in range(levels):
        bids.append(float(data.iloc[frame, data.columns.get_loc(f'bids[{i}].price')]))
        asks.append(float(data.iloc[frame, data.columns.get_loc(f'asks[{i}].price')]))

    asks.reverse()

    for bar, ask, bid in zip(bars, asks, bids):
        bar.set_height(ask)
        bar.set_color('red')
    for bar, bid in zip(bars[levels:], bids):
        bar.set_height(bid)
        bar.set_color('blue')

    return bars, text_time

def midprice_plot():
    mid = [(x + y)/2 for x, y in zip(data['asks[0].price'].tolist(), data['bids[0].price'].tolist())]
    plt.plot(range(len(mid)), mid)
    plt.show()

file_path = 'md2/book_train.parquet'
df = pd.read_parquet(file_path)
data = df.iloc[15700:16100] # choosing time frame with highest price movements dynamics

#midprice_plot()

levels = len(df.columns) // 4 - 2

sup_y = data[f'asks[{levels}].price'].max()
inf_y = data[f'asks[{levels}].price'].min()

xlim = list(range(levels - 1, -1, -1)) + list(range(0, levels))

fig, ax = plt.subplots(figsize=(10, 6))
plt.gcf().set_facecolor('black')
plt.gca().set_facecolor('black')
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)

bars, text_time = init()
ani = FuncAnimation(fig, update, frames=len(data), init_func=init, fargs=(bars, text_time), interval=1)

ani.save('lob.gif', writer='pillow')

plt.show()


