import sqlite3


class Customers:
    def __init__(self):
        self.table = "shop.db"
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
        customer_id INTEGER,
        surname TEXT,
        name TEXT,
        birth_date TEXT,
        country TEXT,
        city TEXT
        )""")
        con.commit()
        con.close()

    def is_new_customer(self, customer_id):
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        ids = cur.execute("""SELECT customer_id FROM customers""").fetchall()
        for c_id in ids:
            if c_id[0] == customer_id:
                con.close()
                print("Customer already exists")
                return False
        con.close()
        print("Customer doesn't exist")
        return True

    def add_customer(self, customer_id, surname, name, birth_date, country, city):
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        cur.execute("""INSERT INTO customers (customer_id, surname, name, birth_date, country, city)
                    VALUES (?, ?, ?, ?, ?, ?)""", (customer_id, surname, name, birth_date, country, city))
        print("Customer was successfully added")
        con.commit()
        con.close()
        return "Вы были успешно зарегистрированы, " + name

    def remove_customer(self, customer_id):
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        cur.execute("""DELETE FROM customers WHERE customer_id=?""", (customer_id,))
        print("Customer was successfully deleted")
        return "Ваш аккаунт был успешно удалён"

    def change_data(self, customer_id, surname, name, birth_date, country, city):
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        cur.execute("""UPDATE customers SET surname=? WHERE customer_id=?""", (surname, customer_id))
        cur.execute("""UPDATE customers SET name=? WHERE customer_id=?""", (name, customer_id))
        cur.execute("""UPDATE customers SET surname=? WHERE birth_date=?""", (birth_date, customer_id))
        cur.execute("""UPDATE customers SET name=? WHERE country=?""", (country, customer_id))
        cur.execute("""UPDATE customers SET name=? WHERE city=?""", (city, customer_id))
        con.commit()
        con.close()
        return "Вы успешно сменили данные аккаунта"

    def get_data(self, customer_id):
        con = sqlite3.connect(self.table)
        cur = con.cursor()
        data = cur.execute("""SELECT surname, name, birth_date, country, city FROM customers WHERE customer_id=?""",
                           (customer_id,)).fetchall()[0]
        print(data)
        con.commit()
        con.close()
        return str(data[0]) + " " + str(data[1]) + "\nДата рождения: " + str(data[2]) + "\nМесто проживания: " + \
            str(data[4]) + ", " + str(data[3])
