import pymongo 

client = pymongo.MongoClient("mongodb+srv://Radswet:AmJjNHkPLn35clNP@cluster0.efbll.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

db = client["Cluster0"]
collection = db["Weplay"]
data = {"name": "fernando"}

collection.insert_one(data)


