import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://gal:dovi140198@cluster0-tb3jj.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = cluster["app"]
collection = db["detailes"]

post1 = {"_id": 1, "Device name": "x", "Version": 3, "Build date": 14}
post2 = {"_id": 2, "Device name": "x", "Version": 4, "Build date": 14}

#collection.insert_one(post)
result = collection.update_one({"_id":0}, {"$set":{"Device name":"Y"}})
