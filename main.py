# EBAY SCRAPPING
# - ALEXANDRE MAGNIER

import csv

import requests
from bs4 import BeautifulSoup

def get_page(url):
    response = requests.get(url)

    if not response.ok:
       print("Server responsed :", response.status_code)
    else:
      soup = BeautifulSoup(response.text,'lxml')
    return soup



def get_detail_data(soup):

  try:
    title = soup.find('h1', id='itemTitle').text.strip('Détails sur  ').replace('\xa0', '')
  except:
    title = ''

  try:
    p = soup.find('span', id='prcIsum').text.strip()
    price, currency = p.split(' ')
  except:
    currency = ''
    price = ''

  try:
    quantity = soup.find('span', id='qtySubTxt').text
  except:
    quantity = ''

  try:
    totalSold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')
  except:
    totalSold = ''

  try: 
    productImage = soup.find('img', id='icImg')
  except:
    productImage = ''

  data = {
    'title': title,
    'price': price,
    'currency': currency,
    'quantity': quantity,
    'total_sold': totalSold,
    'image': productImage['src']
  }

  return data


def get_index_data(soup):
  try:
     links = soup.find_all('a', class_='s-item__link')
  except:
    links = []

  urls = [item.get('href') for item in links]

  return urls


def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
      writer = csv.writer(csvfile)

      row = [data['title'], data['price'], data['currency'], data['quantity'], data['total_sold'], data['image'], url]

      writer.writerow(row)


def main():
    url = 'https://www.ebay.fr/sch/i.html?_from=R40&_trksid=p2380057.m570.l1313&_nkw=pi%C3%A8ces+auto&_sacat=0'

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        write_csv(data, link)
    


if __name__ == '__main__':
  main()