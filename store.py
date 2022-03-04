from Stores.Weplay import discover, products
import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

CONNECTION_STRING = os.getenv('CONNECTION_STRING')

client = pymongo.MongoClient(CONNECTION_STRING)
mydb = client["Cluster0"]
mycol = mydb["Weplay"]

print("Discover")
urls = discover()
aux = 1

print("Products")
for x in urls:
    print(aux , " de ", len(urls))
    product = products(x)
    print(product)
    try:
        product
        mycol.insert_one(product)
    except:
        print("error")