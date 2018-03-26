from flask import Flask, render_template, request, redirect
import quandl
import jinja2
quandl.ApiConfig.api_key = 'oGV1c7rq87zKDJD27zat'
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html, components
from bokeh.resources import CDN
import simplejson as json
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def stockQuery():
  return render_template('stock_ticker_app.html')

@app.route('/index', methods = ['POST', 'GET'])
def index():
  ticker = request.form['ticker']
  myPlot=generateStockPlot(ticker)
  script, div = components(myPlot.p)
  return render_template('bokeh_template.html',div=div, script=script)


class generateStockPlot():
    def __init__(self, ticker):
        self.ticker=ticker
        self.formatTicker()
        thisDate, prevDate= self.getDateRange()
        closingPrices=self.queryStock(thisDate, prevDate)
        self.p=self.makePlot(closingPrices)
        
        
    def makePlot(self, closingPrices):
        dateVec=closingPrices.date
        p = figure(x_axis_type="datetime")
        p.line(closingPrices['date'], closingPrices['close'], line_color="gray", 
            line_width=1, legend=self.ticker)
        p.title.text = "Stock Closing Prices"
        p.xgrid[0].grid_line_color=None
        p.ygrid[0].grid_line_alpha=0.5
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price'        
        return p
       
       
    def formatTicker(self):
        self.ticker=self.ticker.strip()
        self.ticker=self.ticker.upper()
        
        
    def getDateRange(self):
        myDat=datetime.today
        year=myDat().year
        month=myDat().month
        day=myDat().day
        if month==1:
            prevYear=year-1
            prevMonth=12
        else:
            prevYear=year
            prevMonth=month-1
        thisDate=str(year)+'-'+str(month)+'-'+str(day)
        prevDate=str(prevYear)+'-'+str(prevMonth)+'-'+str(day)
        return thisDate, prevDate
    
    
    def queryStock(self, thisDate, prevDate):
        try:
            closingPrices=quandl.get_table('WIKI/PRICES', 
                             qopts = { 'columns': ['date','close'] }, 
                             ticker = [self.ticker], 
                             date = { 'gte': prevDate, 'lte': thisDate })
        except:
            closingPrices=pd.DataFrame.from_dict({'close':['Null'], 'date':['Null']})
        return closingPrices
        
  
if __name__ == '__main__':
  app.run(port=33507)



