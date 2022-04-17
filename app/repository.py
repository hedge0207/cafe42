from bson.objectid import ObjectId
from mongo import mongo_db


def create_admin_post(post):
    mongo_db.db.post.insert_one(dict(post))
    
def get_admin_post(post_id):
    post = mongo_db.db.post.find_one({"_id":ObjectId(post_id)})
    post['_id'] = str(post['_id'])
    return post

def update_admin_post(post_id, post):
    mongo_db.db.post.update_one({"_id":ObjectId(post_id)}, {"$set":dict(post)})

def delete_admin_post(post_id):
    mongo_db.db.post.delete_one({"_id":ObjectId(post_id)})