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
