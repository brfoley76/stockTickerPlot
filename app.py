from flask import Flask, render_template, request, redirect
quandl.ApiConfig.api_key = 'oGV1c7rq87zKDJD27zat'
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN
#import simplejson as json
#import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('stock_ticker_app.html')

if __name__ == '__main__':
  app.run(port=33507)
