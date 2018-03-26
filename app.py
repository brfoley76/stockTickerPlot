from flask import Flask, render_template, request, redirect
import quandl
import jinja2
quandl.ApiConfig.api_key = 'oGV1c7rq87zKDJD27zat'
from bokeh.plotting import figure, output_file, show
from bokeh.embed import file_html
from bokeh.resources import CDN
import simplejson as json
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/')
def index():
  #return render_template('stock_ticker_app.html')
  me=generateStockPlot()
  return render_template(me)
  

if __name__ == '__main__':
  app.run(port=33507)
  
  
class generateStockPlot():
    def __init__(self):
        self.getNewPlot()
        
    def getNewPlot(self):
        myStock=self.getNewStock()
        thisDate, prevDate= self.getDateRange()
        closingPrices=self.queryStock(myStock, thisDate, prevDate)
        self.html=self.makePlot(closingPrices,myStock)
        #self.getNewPlot()
        
        
    def makePlot(self, closingPrices,myStock):
        dateVec=closingPrices.date
        p = figure(x_axis_type="datetime")
        p.line(closingPrices['date'], closingPrices['close'], line_color="gray", line_width=1, legend=myStock)
        p.title.text = "Stock Closing Prices"
        p.xgrid[0].grid_line_color=None
        p.ygrid[0].grid_line_alpha=0.5
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Price'        
        html = file_html(p, CDN, "my plot")
        show(p)
        return html
       
    def getNewStock(self):
        #myStock=raw_input()
        myStock=myStock.strip('googl')
        myStock=myStock.upper()
        return myStock
        
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
    
    def queryStock(self, myStock, thisDate, prevDate):
        try:
            closingPrices=quandl.get_table('WIKI/PRICES', 
                             qopts = { 'columns': ['date','close'] }, 
                             ticker = [myStock], 
                             date = { 'gte': prevDate, 'lte': thisDate })
        except:
            closingPrices=pd.DataFrame.from_dict({'close':['Null'], 'date':['Null']})
        return closingPrices
