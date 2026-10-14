from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient(
    "mongodb://localhost:27017/",
    serverSelectionTimeoutMS=5000
)

db = client["agriagent"]
query_history = db["query_history"]


def test_database_connection():
    client.admin.command("ping")
    return True


def save_query(question, agent, result, details):
    document = {
        "question": question,
        "agent": agent,
        "result": result,
        "farming_details": details,
        "created_at": datetime.now(timezone.utc),
    }

    inserted = query_history.insert_one(document)
    return str(inserted.inserted_id)


def get_recent_queries(limit=10):
    """Return the most recent queries from the query_history collection.

    Args:
        limit (int): Maximum number of records to return (default 10).

    Returns:
        list[dict]: List of records with ObjectId converted to string at key "_id".
    """
    records = query_history.find().sort("created_at", -1).limit(limit)

    history = []

    for record in records:
        record["_id"] = str(record["_id"])
        history.append(record)

    return history

