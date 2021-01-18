# NEWSAPI.ORG SCRAPPING
# - ALEXANDRE MAGNIER

import csv
import urllib
import requests
import json
from bs4 import BeautifulSoup
import urllib.request 
import os.path

def get_page(url):
    response = requests.get(url)

    if not response.ok:
       print("Server responsed :", response.status_code)
    else:
     resultatsApi = response.json()['articles']
    return resultatsApi



def write_csv(data):
    with open('output.csv', 'a') as csvfile:
      writer = csv.writer(csvfile)

    
      
      row = [data['title'],data['description'],data['url'],data['urlToImage'],data['content']]

      writer.writerow(row)


def upload_image(data):

    response = requests.get(data["image"])

    completeName = os.path.join("img/", data["itemnumber"] + ".jpeg")

    file = open(completeName, "wb")
    file.write(response.content)
    file.close()
    

def main():
    url = 'http://newsapi.org/v2/everything?q=football&from=2020-12-18&language=fr&sortBy=publishedAt&apiKey=aa4f9116bd904d7e99c9a24bb49a42a2'

    articles = get_page(url)
    print("articles :  ",articles)
    for d in articles:
     write_csv(d)
  
    


if __name__ == '__main__':
  main()