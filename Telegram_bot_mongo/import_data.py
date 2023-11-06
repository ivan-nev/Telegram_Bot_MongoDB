import bson
from pymongo import MongoClient
from app import Collection
from pathlib import Path

# # Making Connection
# myclient = MongoClient("mongodb://localhost:27017/")
#
# # database
# db = myclient["GFG"]
#
# # Created or Switched to collection
# # names: GeeksForGeeks
# Collection = db["data"]
bson_file = open(Path('dump','sampleDB','sample_collection.bson'), 'rb')
bson_data = bson.decode_all(bson_file.read())
bson_file.close()

Collection.drop()
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else insert_one is used
if isinstance(bson_data, list):
    Collection.insert_many(bson_data)
    print('import ok')
else:
    Collection.insert_one(bson_data)