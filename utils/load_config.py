import json

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_metadata():
    with open("utils/metadata_mongo.json") as f:
        return json.load(f)