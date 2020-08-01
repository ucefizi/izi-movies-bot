import pymongo
import re
from conf.credentials import DB_URL
from conf.model import Movie

client = pymongo.MongoClient(DB_URL)
db = client.movbot


def insert(movie):
    return db.movies.insert_one(movie.__dict__)


def delete_by_name(name, server_id):
    db.movies.delete_one({"name": name, "server_id": server_id})


def delete_by_index(index, server_id):
    db.movies.delete_one({"index": index, "server_id": server_id})


def get_all(server_id):
    results = db.movies.find({"server_id": server_id})

    movies = []
    for result in results:
        movies.append(Movie(**result))

    return sorted(movies, key=lambda mv: (mv.watched, mv.downvotes - mv.upvotes))


def watch_by_name(name, server_id):
    db.movies.update_one({"name": name, "server_id": server_id}, {"$set": {"watched": True}})


def watch_by_index(index, server_id):
    db.movies.update_one({"index": index, "server_id": server_id}, {"$set": {"watched": True}})


def upvote(message_id):
    db.movies.update_one({"message_id": message_id}, {"$inc": {"upvotes": 1}})


def downvote(message_id):
    db.movies.update_one({"message_id": message_id}, {"$inc": {"downvotes": 1}})


def un_upvote(message_id):
    db.movies.update_one({"message_id": message_id}, {"$inc": {"upvotes": -1}})


def un_downvote(message_id):
    db.movies.update_one({"message_id": message_id}, {"$inc": {"downvotes": -1}})


def max_index(server_id):
    try:
        return db.movies.find_one({"server_id": server_id}, sort=[("index", -1)])["index"]
    except:
        return 0


def find_by_name(server_id, name):
    result = db.movies.find_one({'name': re.compile(name, re.IGNORECASE), 'server_id': server_id})
    if result:
        return Movie(**result)
    return None
