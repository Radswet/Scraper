from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)
mydb = client["Cluster0"]
mycol = mydb["CyFstore"]


product_urls = []

website = 'https://fancycustoms.com/collections/keycaps'

result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'html.parser')

while True:
        products = soup.find('div', class_='tt-description')

        if not products:
                break

        for product in products:
                product_urls.append(product['href'])

        print(product_urls)