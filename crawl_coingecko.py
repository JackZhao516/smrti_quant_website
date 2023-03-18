import os
import json
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pycoingecko import CoinGeckoAPI

COINGECKO_API_KEY = json.load(open("token.json"))["COINGECKO_API_KEY"]
cg = CoinGeckoAPI(api_key=COINGECKO_API_KEY)
matplotlib.use('agg')


def get_symbol_id_dict():
    coins = cg.get_coins_list()
    symbol_id_dict = {}
    for coin in coins:
        symbol_id_dict[coin['symbol']] = coin['id']
    return symbol_id_dict


def plot_past_90_days_klines(coins, plot_dir):
    if not os.path.exists(plot_dir):
        os.mkdir(plot_dir)
    for coin_id, name in coins:
        klines = cg.get_coin_market_chart_by_id(id=coin_id.lower(), vs_currency='usd', days=89, interval='hourly')
        klines = klines['prices']

        # save close price vs time plot to directory
        x, y = [], []
        for i, kline in enumerate(klines):
            x.append(datetime.utcfromtimestamp(int(kline[0]) / 1000))
            y.append(float(kline[1]))

        my_dpi = 96
        k = 4
        plt.rc('xtick', labelsize=8 * k)
        plt.rc('ytick', labelsize=8 * k)

        fig, ax = plt.subplots(figsize=(1250 * k / my_dpi, 500 * k / my_dpi), dpi=my_dpi)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        ax.xaxis_date()
        fig.autofmt_xdate()

        plt.plot(x, y, linewidth=1.5)
        plt.title(f'{name.upper()} price vs time', fontsize=10 * k)
        plt.xlabel('Time 90 days ago to now', fontsize=10 * k)

        plt.ylabel('Price in USD', fontsize=10 * k)
        plt.savefig(os.path.join(plot_dir, f'{coin_id}.png'), dpi=my_dpi)
        plt.clf()


if __name__ == '__main__':
    plot_past_90_days_klines([["bitcoin", "BTC"], ["ethereum", "ETH"]], 'plots')
