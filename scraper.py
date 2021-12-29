import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd
from preprocessing import get_type

class RightMoveScraper:
  def __init__(self,pages, location):
    self.location=location
    self.pages= pages 
  results=[]
  
  def fetch(self,url):
    response= requests.get(url)
    return response

  def parse(self,html):
    content= BeautifulSoup(html, 'lxml')
    title= [i.text.strip() for i in (content.select('.propertyCard-title'))]
    address= [i.text.strip() for i in (content.select('.propertyCard-address'))]
    price= [i.text.strip() for i in (content.select('.propertyCard-priceValue'))]
    description= [i.text for i in (content.findAll('span', {'data-test': 'property-description'}))]
    added_on= [i.text.strip().split(' ')[-1] for i in (content.select('.propertyCard-branchSummary-addedOrReduced'))]
    seller= [i.text.strip().split('by')[1].strip() for i in (content.select('.propertyCard-branchSummary'))]
    number= [i.text for i in (content.select('.propertyCard-contactsPhoneNumber'))]
    for index in range(0, len(title)):
      self.results.append({
          'title':title[index],
          'address': address[index],
          'price': price[index],
          'description': description[index],
          'added_on': added_on[index],
          'seller': seller[index],
          'number': number[index],
      })
    self.df= pd.DataFrame(self.results)
    self.df['property_type']= self.df['title'].apply(get_type)
    self.table= self.df.to_html()

  def to_csv(self):
    self.df.to_csv(f'{self.location}_data.csv',index=False)

    

  def run(self):
      for page in range(0, self.pages):
          index = page * 24
          if self.location== 'London':
            url = 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E93917&index=' + str(index) + '&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='
            
            response = self.fetch(url)
            self.parse(response.text)
          if self.location== 'Great Manchester':
            url= 'https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E79192&index=' + str(index) + '&propertyTypes=&mustHave=&dontShow=&furnishTypes=&keywords='
            response = self.fetch(url)
            self.parse(response.text)

      self.to_csv()


#if __name__=="__main__":
#  scraper=RightMoveScraper(5, 'Great Manchester')
#  scraper.run()