from flask import render_template, request,redirect,url_for
import pandas as pd
import requests
import io
from bokeh.embed import components
from bokeh.plotting import figure


api_key='TR6105FS5D9ER94C'

def gen_graph():
    if request.method == "GET":
        return render_template("home.html")
    else:
        symbol = request.form["symbol"]
        form_syear = request.form["start_date"]
        form_eyear = request.form["end_date"]
        closep = request.form.getlist('closing')
        adjclosep = request.form.getlist('adj_closing')
        openp = request.form.getlist('opening')
        adjopenp = request.form.getlist('volume')
        try:
            syear = pd.to_datetime(form_syear)
        except:
            return render_template('invalid.html')
        try:
            eyear = pd.to_datetime(form_eyear)
        except:
            return render_template('invalid.html')
        if syear < pd.to_datetime('02-01-2019') or eyear > pd.to_datetime('01-08-2021'):
            return render_template('invalid.html')
        r = requests.get('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=%s&outputsize=full&apikey=%s&datatype=csv' % (symbol,api_key)).content
        df=pd.read_csv(io.StringIO(r.decode('utf-8')))
        df.timestamp = pd.to_datetime(df.timestamp)
        df = df[(df.timestamp<=eyear)&(df.timestamp>=syear)]
        p=figure(title=symbol,x_axis_type='datetime',plot_height=800,plot_width=1600)
        if closep==['on']:
            p.line(df.timestamp,df.close,color = 'darkred',line_width=3,legend_label='Closing Price',muted_alpha=0.1)
        if openp==['on']:
            p.line(df.timestamp,df.open,color='darkgreen',line_width=3,legend_label='Opening Price',muted_alpha=0.1)
        if adjopenp==['on']:
            p.line(df.timestamp,df.volume,color='cyan',line_width=3,legend_label='Volume',muted_alpha=0.1)
        if adjclosep==['on']:
            p.line(df.timestamp,df.adjusted_close,color='pink',line_width=3,legend_label='Adjusted Closing Price',muted_alpha=0.1)
        if closep==['on'] or openp==['on'] or adjclosep==['on']:
            p.yaxis.axis_label='Price USD'
            if adjopenp==['on']:
                p.yaxis.axis_label='Price USD or Volume #'
        elif adjopenp==['on']:
            p.yaxis.axis_label='Volume #'
        p.xaxis.axis_label ='Date'
        p.legend.location="top_left"
        p.legend.click_policy="mute"
        script,div = components(p)
        return render_template('graph.html',script=script,div=div)

