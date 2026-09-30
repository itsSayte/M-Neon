from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

DATA_FILE = "data/categories.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)


def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            content = f.read().strip()

            if not content:
                return []

            return json.loads(content)

    except:
        return []


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/tree")
def tree():
    return jsonify(load_data())


@app.route("/api/category", methods=["POST"])
def create_category():

    data = load_data()

    data.append({
        "name": request.json["name"],
        "servers": []
    })

    save_data(data)

    return jsonify({"success": True})


@app.route("/api/server", methods=["POST"])
def create_server():

    data = load_data()

    for category in data:

        if category["name"] == request.json["category"]:

            category["servers"].append({

                "name": request.json["name"],
                "type": request.json["type"],
                "version": request.json["version"],
                "ram_min": request.json["ram_min"],
                "ram_max": request.json["ram_max"]

            })

    save_data(data)

    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True)