from Stores.Weplay import discover, products
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://Radswet:AmJjNHkPLn35clNP@cluster0.efbll.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
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