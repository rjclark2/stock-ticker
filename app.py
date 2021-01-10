from flask import Flask, render_template, request, redirect, url_for
from bokeh.embed import components
from bokeh.plotting import figure
import pandas as pd
app = Flask(__name__)

import views

df = pd.DataFrame()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/graph')
def graph():
    from bokeh.plotting import figure
    p = figure()
    script, div = components(p)

    return render_template('graph.html',script=script,div=div)

app.add_url_rule('/', view_func=views.gen_graph, methods=["GET","POST"])

if __name__ == '__main__':
  app.run(port=33507)
