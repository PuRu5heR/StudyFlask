from flask import Flask, render_template, request, redirect, send_from_directory
from store import Store
from customers import Customers
from random import randint
import qrcode
import os

app = Flask(__name__)
urls = []


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test/<arg>")
def test(arg):
    for url in urls:
        if url[1] == arg:
            return redirect(url[0])


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


@app.route("/shorter")
@app.route("/shorter", methods=["POST"])
def shorter():
    if request.method == "POST":
        new_url = ""
        for i in range(5):
            new_url += chr(randint(65, 90))
        urls.append((request.form['url'], new_url))
        return "<a href=http://192.168.58.2:5000/test/" + new_url + ">http://192.168.58.2:5000/test/" + new_url + "</a>"
    return render_template("shorter.html")


@app.route("/upload")
@app.route("/upload", methods=["POST"])
def upload():
    if request.method == "POST":
        request.files['file'].save(os.path.join("files", request.files['file'].filename))
        import qrcode
        QR = qrcode.make("http://192.168.58.2:5000/download/" + request.files['file'].filename)
        QR.save("static\\images\\qr.png")
        return """<img src=/static/images/qr.png alt=QR-код>
        <a href=http://192.168.58.2:5000/download/" + request.files['file'].filename + ">Скачать</a>
        <a href="/">Главная страница</a>"""
    return render_template("upload.html")


@app.route("/download/<file>")
def download(file):
    D = app.root_path + "\\files\\"
    print(D)
    return send_from_directory(directory=D, path=file, as_attachment=True)
    # for files in os.walk(D):
    #     for filename in files:
    #         if filename[0] == file:
    #             pass


@app.route("/computer")
@app.route("/computer/<path:temp>")
def computer(temp=""):
    D = app.root_path
    dir = os.listdir(D)
    out = ""
    for file in dir:
        print(file)
        out += "<a href=http://192.168.58.2:5000/computer/" + file + ">" + file + "</a>\n<br>\n"
    return out


if __name__ == "__main__":
    app.run(host="192.168.58.2", debug=True)
