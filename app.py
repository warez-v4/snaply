from flask import Flask, render_template
from routes.shorten import shorten_bp
from routes.redirect import redirect_bp
from routes.stats import stats_bp

app = Flask(__name__)

app.register_blueprint(shorten_bp)
app.register_blueprint(redirect_bp)
app.register_blueprint(stats_bp)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)