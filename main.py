from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/info")
def info():
    return render_template("info.html")


@app.route("/table")
def table():
    return render_template("table.html")


@app.route("/sql")
def sql():
    return render_template("sql.html")


@app.route("/time")
def time():
    return render_template("time.html")


if __name__ == "__main__":
    app.run(host="192.168.58.2", debug=True)
