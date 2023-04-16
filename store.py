import os
import sqlite3


class Store:
    def __init__(self):
        self.data_base = "shop.db"
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS store (
        customer_id INTEGER,
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT,
        category TEXT,
        product_status TEXT,
        product_price REAL,
        valute TEXT,
        image BLOB)""")
        con.commit()
        con.close()

    def add_product(self, customer_id, product_name, category, product_price_with_valute):
        product_price = float(product_price_with_valute.split(" ")[0])
        valute = product_price_with_valute.split(" ")[1]

        image = open("C:/Users/User/PycharmProjects/Task1/photos/image.jpg", "rb").read()

        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        cur.execute("""INSERT INTO store (customer_id, product_name, category, product_status, product_price,
                    valute, image) VALUES(?, ?, ?, "продаётся", ?, ?, ?)""",
                    (customer_id, product_name, category, product_price, valute, image))

        # i = 0
        # while i < len(images) and i < 10:
        #     cur.execute("""INSERT INTO store (image?) VALUES(?)""", (i, images[i]))
        #     i += 1
        #     print("Photo " + i + " succesfully added")
        os.remove("C:/Users/User/PycharmProjects/Task1/photos/image.jpg")
        print("Product successfully added")
        con.commit()
        con.close()
        return "Товар был успешно добавлен"

    def check_access(self, customer_id, product_id):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        customer_id_real = \
        cur.execute("""SELECT customer_id FROM store WHERE product_id=?""", (product_id,)).fetchall()[0][0]

        if customer_id_real == customer_id:
            print("Access allowed")
            return True
        else:
            print("Access not allowed")
            return False

    def product_exist(self, product_id):
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        products_ids = cur.execute("""SELECT product_id FROM store""").fetchall()
        for pr_id in products_ids:
            if pr_id[0] == int(product_id):
                print("Product exists")
                return True
        print("Product does not exist")
        return False

    def remove_product(self, product_id):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        cur.execute("""DELETE FROM store WHERE product_id=?""", (product_id,))
        print("Product was successfully removed")
        con.commit()
        con.close()
        return "Товар был успешно удалён"

    def remove_all_products(self, customer_id):
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        cur.execute("""DELETE FROM store WHERE customer_id=?""", (int(customer_id),))
        print("Products were successfully removed")
        con.commit()
        con.close()
        return "Товары были успешно удалены"

    def change_product_name(self, product_id, product_name):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        cur.execute("""UPDATE store SET product_name=? WHERE product_id=?""", (product_name, product_id))
        print("Product name was successfully updated")
        con.commit()
        con.close()
        return "Название товара было успешно изменено"

    def change_product_price(self, product_id, product_price_with_valute):
        product_id = int(product_id)
        product_price = float(product_price_with_valute.split(" ")[0])
        valute = product_price_with_valute.split(" ")[1]
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        cur.execute("""UPDATE store SET product_price=? WHERE product_id=?""", (product_price, product_id))
        cur.execute("""UPDATE store SET valute=? WHERE product_id=?""", (valute, product_id))
        print("Product price was successfully updated")
        con.commit()
        con.close()
        return "Цена товара была успешно изменена"

    def change_product_category(self, product_id, category):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        cur.execute("""UPDATE store SET category=? WHERE product_id=?""", (category, product_id))
        print("Category of product name was successfully updated")
        con.commit()
        con.close()
        return "Категория товара была успешно изменена"

    def change_product_status(self, product_id):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()

        status_now = cur.execute("""SELECT status FROM store WHERE product_id=?""", (product_id,))
        if status_now == "продаётся":
            status = "неактивен"
        else:
            status = "продаётся"

        cur.execute("""UPDATE store SET status=? WHERE product_id=?""", (status, product_id))
        print("Status of product name was successfully updated")
        con.commit()
        con.close()
        return "Статус товара был сменён на " + status

    def get_product_status(self, product_id):
        product_id = int(product_id)
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        status_now = cur.execute("""SELECT status FROM store WHERE product_id=?""", (product_id,))

        if status_now == "продаётся":
            return True
        else:
            return False

    def get_products(self):
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        products = cur.execute("""SELECT customer_id, product_id, product_name, category, product_status, 
        product_price, valute, image FROM store""").fetchall()
        for i in range(len(products)):
            photo_path = os.path.join("photos", "image" + str(products[i][1]) + ".jpg")
            open(photo_path, "wb").write(products[i][7])

            # for j in range(9, len(products[i])):
            #     images.append(products[i][j])
            data = cur.execute("""SELECT surname, name, country, city FROM customers WHERE customer_id=?""",
                               (str(products[i][0]),)).fetchall()
            surname = str(data[0][0])
            name = str(data[0][1])
            country = str(data[0][2])
            city = str(data[0][3])
            products[i] = [str(products[i][2]), str(products[i][3]), str(products[i][4]), str(products[i][5]) + " " +
                           str(products[i][6]), surname + " " + name, country + ", " + city, str(products[i][1])]
        return products

    def search_products(self, search_text):
        con = sqlite3.connect(self.data_base)
        cur = con.cursor()
        products = cur.execute("""SELECT customer_id, product_id, product_name, category, product_status, 
        product_price, valute, image FROM store""").fetchall()
        output_products = []
        for i in range(len(products)):
            if search_text in products[i][2]:
                photo_path = os.path.join("photos", "image" + str(products[i][1]) + ".jpg")
                open(photo_path, "wb").write(products[i][7])
                data = cur.execute("""SELECT surname, name, country, city FROM customers WHERE customer_id=?""",
                                   (str(products[i][0]),)).fetchall()
                surname = str(data[0][0])
                name = str(data[0][1])
                country = str(data[0][2])
                city = str(data[0][3])
                output_products.append(
                    [str(products[i][2]), str(products[i][3]), str(products[i][4]), str(products[i][5]) + " " +
                     str(products[i][6]), surname + " " + name, country + ", " + city, str(products[i][1])])
        return output_products


if __name__ == "__main__":
    store = Store()
    print(store.get_products())
