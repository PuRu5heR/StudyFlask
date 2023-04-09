from flask import Flask, render_template, request
from store import Store
from customers import Customers

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
@app.route("/sql", methods=["POST"])
def sql():
    store = Store()
    if request.method == "POST":
        search_text = request.form['search']
        products = store.search_products(search_text)
    else:
        products = store.get_products()
    return render_template("sql.html", products=products, length_list=len(products))


@app.route("/time")
def time():
    return render_template("time.html")


@app.route("/forma")
@app.route("/forma", methods=["POST"])
def forma():
    if request.method == "POST":
        customers = Customers()
        birth_date = request.form['birth_date'].split("-")
        birth_date = birth_date[2] + "." + birth_date[1] + "." + birth_date[0]
        customers.add_customer(0, request.form['surname'], request.form['name'], birth_date, request.form['country'],
                               request.form['city'])
    return render_template("forma.html")


if __name__ == "__main__":
    app.run(host="192.168.58.2", debug=True)
