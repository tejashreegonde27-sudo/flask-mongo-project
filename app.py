from flask import Flask, jsonify, render_template, request, redirect, url_for
from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["flask_db"]
collection = db["users"]

# API route to return JSON data
@app.route("/api")
def api():
    with open("data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# Form page
@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]

            collection.insert_one({
                "name": name,
                "email": email
            })

            return redirect(url_for("success"))

        except Exception as e:
            error = str(e)

    return render_template("index.html", error=error)

# Success page
@app.route("/success")
def success():
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
