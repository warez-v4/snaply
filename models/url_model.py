from pymongo import MongoClient
from config import MONGO_URI, DB_NAME
from datetime import datetime, timezone

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
urls_collection = db["urls"]

# এইখানে বসাও — একবারই রান হবে, ফাইল লোড হওয়ার সময়
urls_collection.create_index("created_at", expireAfterSeconds=180)


def save_url(short_code, original_url):
    urls_collection.insert_one({
        "short_code": short_code,
        "original_url": original_url,
        "clicks": 0,
        "created_at": datetime.now(timezone.utc)
    })


def get_original_url(short_code):
    result = urls_collection.find_one({"short_code": short_code})
    if result:
        return result["original_url"]
    return None


def code_exists(short_code):
    return urls_collection.find_one({"short_code": short_code}) is not None


def increment_clicks(short_code):
    urls_collection.update_one(
        {"short_code": short_code},
        {"$inc": {"clicks": 1}}
    )