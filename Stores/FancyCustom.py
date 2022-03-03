from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient(
    "mongodb+srv://Radswet:AmJjNHkPLn35clNP@cluster0.efbll.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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