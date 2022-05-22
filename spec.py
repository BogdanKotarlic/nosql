import json

def load_spec(path="mysql_spec.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)