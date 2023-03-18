
import os
import glob

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from crawl_coingecko import get_symbol_id_dict, plot_past_90_days_klines

app = Flask(__name__)
app.config['PLOTS'] = 'static'


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/queryList', methods=['POST'])
def query_list():
    folder = app.config['PLOTS']
    name = request.form.get('name')
    symbol_2_id = get_symbol_id_dict()

    if not os.path.exists(folder):
        os.mkdir(folder)
    else:
        files = glob.glob(f'{folder}/*')
        for f in files:
            os.remove(f)

    if not name:
        return error_handler('No name provided')
    name = name.strip().split(' ')
    for n in name:
        n = n.lower()
        if n not in symbol_2_id:
            return error_handler('No such coin: ' + n)

    for n in name:
        n = n.lower()
        plot_past_90_days_klines([[symbol_2_id[n], n]], folder)

    files = os.listdir(folder)

    return render_template('plot.html', plots=files)


@app.route('/uploads/<filename>')
def get_img(filename):
    """Get static file."""
    return send_from_directory(
        app.config['PLOTS'], filename)


def error_handler(error_message):
    return f"<html>{error_message}</html>"


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 4000))
    app.run(host='0.0.0.0', port=port)
