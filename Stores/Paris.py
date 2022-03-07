from math import prod
from bs4 import BeautifulSoup
from numpy import size
import requests
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)

mydb = client["Paris"]

product_urls = []

website = 'https://www.paris.cl/{}/{}/{}/?start={}&sz={}'

categoria="tecnologia"
subcategoria="celulares"
tipo="smartphones"
start = 0 # 40 en 40
sz = 40
mycol = mydb[categoria]
while True:
    url = website.format(categoria,subcategoria,tipo,start,size)      
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')

    product = soup.findAll('div',class_="main")
    start +=40
    if not product:
        break
    for p in product:
        product_urls.append(p.find('a')['href'])
        #print(p.find('a')['href'])
    #print(start)
    
website = 'https://www.paris.cl{}'


for urls in product_urls:
    url = website.format(urls)    
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    
    name = soup.find('h1',{"itemprop":"name"}).text.strip()
    price = soup.find('div',class_="price__text").text.strip()
    brand = soup.find('a',{"id":"GTM_pdp_brand"}).text
    sku = soup.find('div',class_="col-xs-6 col-xs-6 col-sm-6 col-md-6 col-lg-6 pdp-sku").find('p').text.replace("SKU ","")    

    try:
        price_sm = soup.find('div',class_="price__text-sm").text.strip()
        data = {"name":name,"price":price,"price-sm":price_sm,"brand":brand,"sku":sku,"url":url}
    except:
        data = {"name":name,"price":price,"brand":brand,"sku":sku,"url":url}
    print(data)
    mycol.insert_one(data)
