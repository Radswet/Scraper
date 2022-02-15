from bs4 import BeautifulSoup
import requests
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient(
    "mongodb+srv://Radswet:AmJjNHkPLn35clNP@cluster0.efbll.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
mydb = client["Cluster0"]
mycol = mydb["LaCasaDeLaReposteria"]

website = 'https://www.lacasadelareposteria.cl/product-category/articulos-cumpleanos/'


result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'html.parser')


categories_urls = []
categories = soup.find('ul', class_='product-categories')

for category in categories.find_all('a', href=True):
    categories_urls.append(category['href'])


products_urls = []

for category_url in categories_urls:
    result = requests.get(category_url)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')

    products = soup.findAll(
        'a', class_='thumb-link woocommerce-product-gallery__image')

    if not products:
        break

    for product in products:
        products_urls.append(product['href'])


for url in products_urls:
    result = requests.get(url)
    content = result.text
    soup = BeautifulSoup(content, 'html.parser')

    try:
        name = soup.find('h1', class_='product_title entry-title').text
        price = soup.find('p', class_='price').text

        print(name+" "+price)

        data = {"name": name, "price": price, "url": url}
        mycol.insert_one(data)

    except:
        print("error 404")