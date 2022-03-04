from math import prod
from bs4 import BeautifulSoup
import requests
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

def categories():
    return [
        "artisans",
        "deskmats-1",
        "keycaps",
        "switches",
        "placas",
        "pcb",
        "carcasas",
        "accesorios",
        "cables",
        "servicios",
        "gb-keycaps",
        "teclados",
        "gb-switches",
        "extras",
        "kits",
    ]


CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)

mydb = client["Cluster0"]
mycol = mydb["FancyCustom"]


product_urls = []

website = 'https://fancycustoms.com/collections/{}'
categories = categories()


for category in categories:
        url = website.format(category)      
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')

        product = soup.findAll('h2',class_="tt-title prod-thumb-title-color")
        
        for p in product:
                product_urls.append(p.find('a')['href'].replace("/collections/", ""))
                #print(p.find('a')['href'].replace("/collections/", ""))

for urls in product_urls:
        url = website.format(urls)    
        result = requests.get(url)
        soup = BeautifulSoup(result.text, 'html.parser')

        name = soup.find('h1',class_="tt-title").text
        try:
                price = soup.find('span',class_="new-price").text
                data = {"name":name,"price":price}
        except:
                sale = soup.find('span',class_="sale-price").text
                old = soup.find('span',class_="old-price").text
                data = {"name":name,"sale-price":sale,"old-price":old}

        mycol.insert_one(data)