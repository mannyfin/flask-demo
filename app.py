from flask import Flask, render_template, request, redirect
from bokeh.plotting import figure
# from bokeh.models.widgets import Select, TextInput
from bokeh.models.widgets.inputs import TextInput
from bokeh.models import CustomJS
from bokeh.resources import CDN
from bokeh.embed import file_html, json_item, components
import os
import numpy as np
import json
import pandas as pd
import quandl
from bokeh.layouts import column, row


quandl.ApiConfig.api_key='xAsfBK8V2f8RbfWshign'
app = Flask(__name__)

ticker_list = pd.read_csv('WIKI_metadata.csv', usecols=['code']).values

def check_ticker(ticker):
    ticker_list = pd.read_csv('WIKI_metadata.csv', usecols=['code']).values
    if ticker in ticker_list:
        return True
    return False


def create_fig(ticker,start_date='2018-01-01', end_date='2018-03-04'):
    if start_date is None and end_date is None:
        start_date = '2018-01-01'
        end_date = '2018-03-04'
    elif (start_date is None or start_date is '') and (end_date is None or end_date is ''):
        start_date = '2018-01-01'
        end_date = '2018-03-04'
    elif (end_date is None or end_date is '') and (start_date is not None and start_date is not ''):
        # if only start date is specified
        start_date = pd.to_datetime(start_date)
        end_date = start_date + pd.DateOffset(30)
    elif (start_date is None or start_date is '') and (end_date is not None and end_date is not ''):
        # only end date specified
        end_date = pd.to_datetime(end_date)
        start_date = end_date + pd.DateOffset(-30)
    elif isinstance(start_date,str) and isinstance(end_date,str):
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)

    if check_ticker(ticker):
        df = quandl.get('WIKI/'+ticker, start_date=start_date, end_date=end_date).Close
    else:
        return
    # try:
    assert type(df) == pd.core.series.Series, 'uh oh'
    title='myplot'
    TOOLS = 'pan, wheel_zoom, box_zoom, reset, save, crosshair'
    p = figure(tools=TOOLS, plot_width=800, plot_height=350, x_axis_type='datetime')
    p.line(df.index, df.values, color='red',)
    p.title.text = ticker+' close price'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    return p

def text_box(text=None):
    tbox = TextInput(title='StockSTUFF', value=text)
    return tbox


@app.route('/', methods=['POST', 'GET'])
def index():
    try:
        text_val = request.args.get('stock')
        # text_val = t.value
        if text_val is None or text_val is '':
            text_val = 'GOOG'
            t = text_box(text_val)

        start_date = request.args.get('startdate')
        end_date = request.args.get('enddate')
        t = text_box(text_val)

        plot = create_fig(text_val,start_date, end_date)
        # hover = create_hover_tool()
        script, div = components(plot)

        return render_template('index.html', script=script, div=div, feature_names=ticker_list, current_feature_name=text_val)
    except:
        return 'hi'

if __name__ == '__main__':
    app.run(port=33507, debug=True)
    # app.run()


