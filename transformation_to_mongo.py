import pymongo
import json
import mysql_functions

def connection(host):
    my_client = pymongo.MongoClient("mongodb://"+host)
    return my_client

def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_spec(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config("config files/mysql_config.json")
mysql_functions.connection(config["host"], config["user"], config["password"])
my_client = connection(load_config()["host"])

relationships = load_spec("example_mysql.json")

doc = load_spec("example.json")
print(doc)

database = "upravljanje_projektom"
table = list(doc.keys())[0]
print(table)
result_doc = {"title":table}
data = mysql_functions.search(database, table, doc[table]["columns"], doc[table]["values"]).fetchall()
for t in doc[table]["content"]:
    content = mysql_functions.search(database, t, [relationships[t][table]], doc[table]["values"]).fetchall()
    print(content)
    result_doc[t]=content


with open("result_doc.json", "w", encoding="utf-8") as f:
    json.dump(result_doc, f)
#example_mysql mogu sve relacije da ubacim


#mogu vec ime baze nabaviti pre nego se selektuje example.json
#my_db = my_client["my_database"]
#my_col = my_db["docs"]
#my_col.insert_one(result_doc)