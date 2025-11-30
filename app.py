from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route("/")
def index():
    with open("data/stats.json") as f:
        stats = json.load(f)
    return render_template("index.html", stats=stats)
