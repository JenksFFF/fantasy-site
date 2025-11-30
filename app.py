
from flask import Flask, render_template
from stats import get_fantasy_stats

app = Flask(__name__)

@app.route("/")
def index():
    stats = get_fantasy_stats()
    return render_template("index.html", stats=stats)

@app.route("/refresh")
def refresh():
    stats = get_fantasy_stats()
    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from stats import get_fantasy_stats

app = Flask(__name__)

@app.route("/")
def index():
    stats = get_fantasy_stats()
    return render_template("index.html", stats=stats)

@app.route("/refresh")
def refresh():
    stats = get_fantasy_stats()
    return render_template("index.html", stats=stats)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's PORT
    app.run(host="0.0.0.0", port=port)
