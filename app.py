from flask import Flask
from flask import render_template
from flask import request
from flask import send_from_directory
from scraper import *
import pandas as pd
from preprocessing import get_type
from clean import clean_price


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('home.html')

@app.route('/results',methods=['GET', 'POST'])
def results():
    if request.method=="POST":
        location= request.form.get('location')
        pages= int(request.form.get('pages'))



        scraper = RightMoveScraper(location=location,pages=pages)
        scraper.run()
        df= pd.DataFrame(scraper.results)
        df['property_type']= df['title'].apply(get_type)
        df['price']= df['price'].apply(clean_price)
        #df['added_on']= pd.to_datetime(df['added_on'], format='%Y-%m-%d')
        table= df.to_html()
        df.to_csv('downloadable.csv', index=False)
    return render_template('results2.html', tables=[df.to_html(classes='data')], titles=df.columns.values, row_data=list(df.values.tolist()), location=location)
    

@app.route('/test', methods= ['POST', 'GET'])
def test():
    if request.method=="POST":
        location= request.form.get('location')
        pages= request.form.get('pages')
    return render_template('test.html',location=location, pages=pages)

@app.route('/download')
def download():
    return send_from_directory('', 'downloadable.csv', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)