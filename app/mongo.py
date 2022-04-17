from pymongo import MongoClient

from config import config


class MongoDB:
    client = MongoClient
    db = None

mongo_db = MongoDB()


def connect_mongo():
    mongo_db.client = MongoClient(config.mongo_url)
    mongo_db.db = mongo_db.client['cafe42']

def disconect_mongo():
    if mongo_db.client:
        mongo_db.client.close()
