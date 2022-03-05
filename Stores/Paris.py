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

mydb = client["Cluster0"]
mycol = mydb["Paris"]


product_urls = []

website = 'https://www.paris.cl/{}/{}/{}/?start={}&sz={}'

categoria="tecnologia"
subcategoria="celulares"
tipo="smartphones"
start = 0 # 40 en 40
sz = 40
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
    print(url)
    name = soup.find('h1',{"itemprop":"name"}).text
    price = soup.find('div',class_="price__text").text
    try:
        price_sm = soup.find('div',class_="price__text-sm").text
        data = {"name":name.strip(),"price":price.strip(),"price-sm":price_sm.strip()}
    except:
        data = {"name":name.strip(),"price":price.strip()}
    mycol.insert_one(data)
