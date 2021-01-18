# NEWSAPI.ORG SCRAPPING
# - ALEXANDRE MAGNIER

import csv
import urllib
import requests
import json
from bs4 import BeautifulSoup
import urllib.request 
import os.path
from os import path

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

    response = requests.get(data["urlToImage"])
    print('response img : ',response.text)
    completeName = os.path.join("img/", data["urlToImage"])

    file = open(completeName, "wb")
    file.write(response.content)
    file.close()


def get_image(image_url):
    """
    Get image based on url.
    :return: Image name if everything OK, False otherwise
    """
    image_name = path.split(image_url)[1]
    try:
        image = requests.get(image_url)
    except OSError:  # Little too wide, but work OK, no additional imports needed. Catch all conection problems
        return False
    if image.status_code == 200:  # we could have retrieved error page
        base_dir = path.join(path.dirname(path.realpath(__file__)), "img") # Use your own path or "" to use current working directory. Folder must exist.
        with open(path.join(base_dir, image_name), "wb") as f:
            f.write(image.content)
        return image_name

def main():
    url = 'http://newsapi.org/v2/everything?q=football&from=2020-12-18&language=fr&sortBy=publishedAt&apiKey=aa4f9116bd904d7e99c9a24bb49a42a2'

    articles = get_page(url)
    print("articles :  ",articles)
    for d in articles:
     write_csv(d)
     try:
       get_image(d['urlToImage'])
     except:
       get_image('https://www.bankoffootball.com/themes/wowonder/img/130xNxlogo.png.pagespeed.ic.p4RSVnbpN5.webp')
  
    


if __name__ == '__main__':
  main()