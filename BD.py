import psycopg2

class Database:

    def drop_db(self):
        with conn.cursor() as cur:
            cur.execute("""
            DROP TABLE clientphone;
            DROP TABLE phone;
            DROP TABLE client;
            """)
            conn.commit()

    def create_db(self):
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS client(name VARCHAR(40), surname VARCHAR(40), email VARCHAR(40) PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS phone(number VARCHAR(40) PRIMARY KEY);
            CREATE TABLE IF NOT EXISTS clientphone(client_email VARCHAR(40) REFERENCES client(email), client_phone VARCHAR(40) REFERENCES phone(number), CONSTRAINT pk PRIMARY KEY (client_email, client_phone));
            """)
            conn.commit()
        print("Create")

    def add_client(self, name, surname, email, phone=None):
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO client(name, surname, email) VALUES(%s, %s, %s);""", (name, surname, email,))
            if phone != None:
                cur.execute("""INSERT INTO phone(number) VALUES(%s);""", (phone,))
                cur.execute("""INSERT INTO clientphone(client_email, client_phone) VALUES(%s, %s);""", (email, phone,))
            cur.execute("""SELECT c.name, c.surname, c.email, p.client_phone FROM client c LEFT JOIN clientphone p ON c.email = p.client_email WHERE email=%s;""", (email,))
            print(cur.fetchall())
            conn.commit()

    def add_phone(self, email, phone):
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO phone(number) VALUES(%s);""", (phone,))
            cur.execute("""INSERT INTO clientphone(client_email, client_phone) VALUES(%s, %s);""", (email, phone,))
            cur.execute("""SELECT c.name, c.surname, c.email, p.client_phone FROM client c LEFT JOIN clientphone p ON c.email = p.client_email WHERE email=%s;""", (email,))
            print(cur.fetchall())
            conn.commit()

    def change_client(self, email, name=None, surname=None, phone=None):
        with conn.cursor() as cur:
            if name != None:
                cur.execute("""UPDATE client SET name=%s WHERE email=%s;""", (name, email,))
            if surname != None:
                cur.execute("""UPDATE client SET surname=%s WHERE email=%s;""", (surname, email,))
            if phone != None:
                cur.execute("""INSERT INTO phone(number) VALUES(%s);""", (phone,))
                cur.execute("""UPDATE clientphone SET client_phone=%s WHERE client_email=%s;""", (phone, email,))
            cur.execute("""SELECT c.name, c.surname, c.email, p.client_phone FROM client c LEFT JOIN clientphone p ON c.email = p.client_email WHERE email=%s;""", (email,))
            print(cur.fetchall())
            conn.commit()

    def delete_phone(self, email, phone):
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM clientphone WHERE client_phone=%s AND client_email=%s;""", (phone, email,))
            cur.execute("""DELETE FROM phone WHERE number=%s;""", (phone,))
            cur.execute("""SELECT c.name, c.surname, c.email, p.client_phone FROM client c LEFT JOIN clientphone p ON c.email = p.client_email WHERE email=%s;""", (email,))
            print(cur.fetchall())
            conn.commit()

    def delete_client(self, email):
        with conn.cursor() as cur:
            cur.execute("""DELETE FROM clientphone WHERE client_email=%s;""", (email,))
            cur.execute("""DELETE FROM client WHERE email=%s;""", (email,))
            conn.commit()

    def find_client(self, name=None, surname=None, email=None, phone=None):
        with conn.cursor() as cur:
            where = ""
            dts = []
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
                where = where + "client_phone=%s and "
                dts.append(phone)
            dts_tup = tuple(dts)
            cur.execute(f"""SELECT c.name, c.surname, c.email, p.client_phone FROM client c LEFT JOIN clientphone p ON c.email = p.client_email WHERE {where}1!=0;""", dts_tup)
            print(cur.fetchall())
            conn.commit()


if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="Icx5Fm7Xy87") as conn:
        db_client = Database()
        db_client.drop_db()
        db_client.create_db()

        print("Клиенты добавлены:")
        db_client.add_client("Jonn", "Wain", "JW@g.ru")
        db_client.add_client("Stan", "Lee", "SL@g.com")
        db_client.add_client("Piter", "Jonson", "PJ@n.com", "55555")
        db_client.add_client("Gus", "Jonson", "GJ@s.com", "11111")

        print("Телефоны добавлены:")
        db_client.add_phone("SL@g.com", "22222")
        db_client.add_phone("PJ@n.com", "55554")

        print("Клиенты изменены:")
        db_client.change_client("SL@g.com", phone="33333")
        db_client.change_client("JW@g.ru", "Jonny", "Waine",)

        print("Телефоны удалены:")
        db_client.delete_phone("SL@g.com", "22222")

        print("Клиенты удалены")
        db_client.delete_client("GJ@s.com")

        print("Результат поиска:")
        db_client.find_client("Piter", "Jonson", "PJ@n.com")
        db_client.find_client(phone="55554")
        db_client.find_client(name="Stan")
        db_client.find_client(surname="Jonson")
    conn.close()
