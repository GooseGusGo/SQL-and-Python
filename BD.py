import psycopg2

class Database:

    def drop_db(self):
        cur.execute("""
        DROP TABLE phone;
        DROP TABLE client;
        """)
        conn.commit()

    def create_db(self):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS client(id INTEGER PRIMARY KEY, name VARCHAR(40), surname VARCHAR(40), email VARCHAR(40));
        CREATE TABLE IF NOT EXISTS phone(id INTEGER PRIMARY KEY, number VARCHAR(40), id_client INTEGER REFERENCES client(id));
        """)
        conn.commit()
        print("Create")

    def add_client(self, id_client, name, surname, email, id_phone=None, phone=None):
        cur.execute("""INSERT INTO client(id, name, surname, email) VALUES(%s, %s, %s, %s);""", (id_client, name, surname, email,))
        if phone != None:
            cur.execute("""INSERT INTO phone(id, number, id_client) VALUES(%s, %s, %s);""", (id_phone, phone, id_client))
        cur.execute("""SELECT c.name, c.surname, c.email, p.number FROM client c LEFT JOIN phone p ON c.id = p.id_client WHERE c.id=%s;""", (id_client,))
        print(cur.fetchall())
        conn.commit()

    def add_phone(self, id_phone, phone, id_client):
        cur.execute("""INSERT INTO phone(id, number, id_client) VALUES(%s, %s, %s);""", (id_phone, phone, id_client))
        cur.execute("""SELECT c.name, c.surname, c.email, p.number FROM client c LEFT JOIN phone p ON c.id = p.id_client WHERE c.id=%s;""", (id_client,))
        print(cur.fetchall())
        conn.commit()

    def change_client(self, id_client, name=None, surname=None, email=None, id_phone=None, phone=None):
        if email != None:
            cur.execute("""UPDATE client SET email=%s WHERE id=%s;""", (email, id_client,))
        if name != None:
            cur.execute("""UPDATE client SET name=%s WHERE id=%s;""", (name, id_client,))
        if surname != None:
            cur.execute("""UPDATE client SET surname=%s WHERE id=%s;""", (surname, id_client,))
        if id_phone != None and phone != None:
            cur.execute("""INSERT INTO phone(id, number, id_client) VALUES(%s, %s, %s);""", (id_phone, phone, id_client))
        cur.execute("""SELECT c.name, c.surname, c.email, p.number FROM client c LEFT JOIN phone p ON c.id = p.id_client WHERE c.id=%s;""", (id_client,))
        print(cur.fetchall())
        conn.commit()

    def delete_phone(self, id_phone, phone, id_client):
        cur.execute("""DELETE FROM phone WHERE id=%s;""", (id_phone,))
        cur.execute("""SELECT c.name, c.surname, c.email, p.number FROM client c LEFT JOIN phone p ON c.id = p.id_client WHERE c.id=%s;""", (id_client,))
        print(cur.fetchall())
        conn.commit()

    def delete_client(self, id_client):
        cur.execute("""DELETE FROM phone WHERE id_client=%s;""", (id_client,))
        cur.execute("""DELETE FROM client WHERE id=%s;""", (id_client,))
        conn.commit()

    def find_client(self, id_client=None, name=None, surname=None, email=None, phone=None):
        where = ""
        dts = []
        if id_client != None:
            where = where + "c.id=%s and "
            dts.append(id_client)
        if name != None:
            where = where + "name=%s and "
            dts.append(name)
        if surname != None:
            where = where + "surname=%s and "
            dts.append(surname)
        if email != None:
            where = where + "email=%s and "
            dts.append(email)
        if phone != None:
            where = where + "number=%s and "
            dts.append(phone)
        dts_tup = tuple(dts)
        cur.execute(f"""SELECT c.name, c.surname, c.email, p.number FROM client c LEFT JOIN phone p ON c.id = p.id_client WHERE {where}1!=0;""", dts_tup)
        print(cur.fetchall())
        conn.commit()


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="Icx5Fm7Xy87") as conn:
        with conn.cursor() as cur:
            db_client = Database()
            db_client.drop_db()
            db_client.create_db()

            print("Клиенты добавлены:")
            db_client.add_client("1", "Jonn", "Wain", "JW@g.ru")
            db_client.add_client("2", "Stan", "Lee", "SL@g.com")
            db_client.add_client("333", "Piter", "Jonson", "PJ@n.com", "1", "55555")
            db_client.add_client("4", "Gus", "Jonson", "GJ@s.com", "2", "11111")

            print("Телефоны добавлены:")
            db_client.add_phone("4", "22222", "2")
            db_client.add_phone("3", "55554", "333")

            print("Клиенты изменены:")
            db_client.change_client("2", id_phone="7", phone="33333")
            db_client.change_client("1", "Jonny", "Waine",)

            print("Телефоны удалены:")
            db_client.delete_phone("4", "22222", "2")

            print("Клиенты удалены")
            db_client.delete_client("4")

            print("Результат поиска:")
            db_client.find_client("333", "Piter", "Jonson", "PJ@n.com")
            db_client.find_client(phone="55554")
            db_client.find_client(name="Stan")
            db_client.find_client(surname="Jonson")
    conn.close()
