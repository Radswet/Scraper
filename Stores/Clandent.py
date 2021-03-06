from bs4 import BeautifulSoup
import requests
import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)
mydb = client["Cluster0"]
mycol = mydb["Clandent"]


website = 'https://www.clandent.cl/product-category/radiologia/?v=cda73baae416'

result = requests.get(website)
soup = BeautifulSoup(result.text, 'html.parser')

Categories = soup.findAll('li', class_='cat-item')

Categories_urls = []

for c in Categories:
    if not 'universidades' in c.find('a')['href']:
        Categories_urls.append(c.find('a')['href'])

Products_urls = []

for url in Categories_urls:
    result = requests.get(url)
    soup = BeautifulSoup(result.text, 'html.parser')
    Product = soup.findAll('div', class_='product-wrapper')

    for p in Product:
        Products_urls.append(p.find('a')['href'])
    print(Products_urls)

for url in Products_urls:
    try:
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')

        brand = soup.find('div', {'class':'product-brands'}).text
        
        name = soup.find('h1', class_='product_title entry-title').text
        price = soup.find('bdi').text
        sku = soup.find('span', {'class': 'sku'}).text

        Product = {'Brand':brand,'Name':name,'Price':price,'SKU':sku,'URL':url}
        print(Product)
        mycol.insert_one(Product)
    except:
        print("404")

