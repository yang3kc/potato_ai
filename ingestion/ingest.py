import pandas as pd
from pymongo import MongoClient
import os


def ingest_data(file_path):
    # Connect to MongoDB
    client = MongoClient(
        os.environ.get("MONGODB_URI", "mongodb://localhost:27017/potato")
    )
    db = client.potato
    tweets = db.tweets

    # Read TSV file
    df = pd.read_csv(file_path, sep="\t")

    # Convert DataFrame to list of dictionaries
    tweets_data = df.to_dict("records")

    # Insert data into MongoDB
    result = tweets.insert_many(tweets_data)
    print(f"Inserted {len(result.inserted_ids)} documents")


if __name__ == "__main__":
    ingest_data("path_to_your_tsv_file.tsv")
