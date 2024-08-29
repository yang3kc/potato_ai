from flask import Blueprint, request, jsonify
from pymongo import MongoClient
import os

search_bp = Blueprint("search", __name__)
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/potato"))
db = client.potato


@search_bp.route("/search", methods=["GET"])
def search():
    """
    Perform a search query on tweets and return aggregated results.

    This endpoint searches for tweets containing the specified term and returns
    aggregated statistics including tweet count, unique users, average likes,
    and place IDs.

    Query Parameters:
    - term (str): The search term to look for in tweets.

    Returns:
    - JSON: Aggregated search results or an error message.
    """
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "No search term provided"}), 400

    # Perform search query
    results = db.tweets.aggregate(
        [
            {"$match": {"text": {"$regex": term, "$options": "i"}}},
            {
                "$group": {
                    "_id": None,
                    "tweet_count": {"$sum": 1},
                    "unique_users": {"$addToSet": "$user_id"},
                    "avg_likes": {"$avg": "$favorite_count"},
                    "place_ids": {"$addToSet": "$place_id"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "tweet_count": 1,
                    "unique_users": {"$size": "$unique_users"},
                    "avg_likes": 1,
                    "place_ids": 1,
                }
            },
        ]
    )

    result = list(results)[0] if results.alive else {}
    return jsonify(result)


@search_bp.route("/search/daily", methods=["GET"])
def search_daily():
    """
    Perform a daily search query on tweets and return results grouped by date.

    This endpoint searches for tweets containing the specified term and returns
    the tweet count for each day.

    Query Parameters:
    - term (str): The search term to look for in tweets.

    Returns:
    - JSON: List of daily tweet counts or an error message.
    """
    term = request.args.get("term", "")
    if not term:
        return jsonify({"error": "No search term provided"}), 400

    # Perform daily search query
    results = db.tweets.aggregate(
        [
            {"$match": {"text": {"$regex": term, "$options": "i"}}},
            {
                "$group": {
                    "_id": {
                        "$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}
                    },
                    "tweet_count": {"$sum": 1},
                }
            },
            {"$sort": {"_id": 1}},
        ]
    )

    return jsonify(list(results))
