import pymongo
import json
import mysql_functions
import config

def connection(host):
    my_client = pymongo.MongoClient("mongodb://"+host)
    return my_client

def load_config(path="mongodb_config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_spec(path="mongodb_spec.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

config = config.load_config("mysql_config.json")
mysql_functions.connection(config["host"], config["user"], config["password"])
my_client = connection(load_config()["host"])

relationships = load_spec("example_mysql.json")

doc = load_spec("example.json")
print(doc)

database = "asdf"
table = list(doc.keys())[0]
result_doc = {"title":table}
data = mysql_functions.search(database, table, doc[table]["columns"], doc[table]["values"]).fetchall()
for t in doc[table]["content"]:
    content = mysql_functions.search(database, t, [relationships[t][table]], doc[table]["values"]).fetchall()
    result_doc[t]=content


with open("result_doc.json", "w", encoding="utf-8") as f:
    json.dump(result_doc, f)

my_db = my_client["my_database"]
my_col = my_db["docs"]
my_col.insert_one(result_doc)