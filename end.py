from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/random-item")
def random_item():
    import random
from notion_client import Client

notion = Client(auth="secret_CHdDdchMswpXWV8vrjSHZkC7aDRYAR0xZWHof8fJ6Ay")

database1_id = "6024a1e6510646b2bc0521ca4ca7eda9?v"
database2_id = "0ca392e2b54b4dad997cc01cc32af946?v"

results1 = notion.databases.query(
    **{
        "database_id": database1_id,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ]
    }
).get("results")

results2 = notion.databases.query(
    **{
        "database_id": database2_id,
        "sorts": [
            {
                "property": "Name",
                "direction": "ascending"
            }
        ]
    }
).get("results")

all_results = results1 + results2

random_item = random.choice(all_results)

print(random_item)
    return jsonify({"result": random_item})

if __name__ == "__main__":
    app.run()
