import os
import json
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/" 
DATABASE_NAME = "$DatabaseName"     

FOLDER_PATH = "./$FolderPath"   

def load_json_files_to_mongodb(folder_path, mongo_uri, database_name):
    client = MongoClient(mongo_uri)
    db = client[database_name]
    
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            collection_name = os.path.splitext(filename)[0]  
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    collection = db[collection_name]  
                    if isinstance(data, list): 
                        collection.insert_many(data)
                    else:  
                        collection.insert_one(data)
                    print(f"Successfully inserted data into collection: {collection_name}")
                except Exception as e:
                    print(f"Error inserting data from {filename} into collection {collection_name}: {e}")

    client.close()

load_json_files_to_mongodb(FOLDER_PATH, MONGO_URI, DATABASE_NAME)
