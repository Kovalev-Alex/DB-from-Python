import psycopg


def create_db(conn):
    with conn.cursor() as cur:
        # Создание таблиц.
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(40),
                last_name VARCHAR(40)
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS email(
                id SERIAL PRIMARY KEY,
                email VARCHAR(80) NULL
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                phone VARCHAR(20) NULL
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients_email(
                client_id INTEGER REFERENCES client(id),
                email_id INTEGER NULL REFERENCES email(id),
                PRIMARY KEY (client_id, email_id)
            );""")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients_phone(
                client_id INTEGER REFERENCES client(id),
                phone_id INTEGER NULL REFERENCES phone(id),
                PRIMARY KEY (client_id, phone_id)
            );""")
        conn.commit()


def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client (first_name, last_name)
                VALUES (%s, %s) RETURNING id;
            """, (first_name, last_name,))
        client_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO email (email)
                VALUES (%s) RETURNING id;
            """, (email,))
        email_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO phone (phone)
                VALUES (%s) RETURNING id;
            """, (phones,))
        phone_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO clients_email (client_id, email_id)
                VALUES (%s, %s);
            """, (client_id, email_id,))
        cur.execute("""
            INSERT INTO clients_phone (client_id, phone_id)
                VALUES (%s, %s);
            """, (client_id, phone_id,))
        conn.commit()


def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone (phone)
                 VALUES (%s) RETURNING id;
                """, (phone,))
        phone_id = cur.fetchone()[0]
        cur.execute("""
            INSERT INTO clients_phone (client_id, phone_id)
                VALUES (%s, %s);
            """, (client_id, phone_id,))
        conn.commit()


def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        if first_name is not None:
            cur.execute("""
                UPDATE client SET first_name=%s 
                    WHERE id=%s;
                    """, (first_name, client_id,))
        if last_name is not None:
            cur.execute("""
                UPDATE client SET  last_name=%s 
                    WHERE id=%s;
                    """, (last_name, client_id,))
        if email is not None:
            cur.execute("""
                SELECT email_id FROM clients_email
                    WHERE client_id = %s;
                """, (client_id,))
            email_id = cur.fetchone()[0]
            cur.execute("""
                UPDATE email SET email=%s 
                    WHERE id=%s;
                    """, (email, email_id,))
        if phones is not None:
            cur.execute("""
                 SELECT phone_id FROM clients_phone
                    WHERE client_id = %s;
                    """, (client_id,))
            phone_id = cur.fetchone()[0]
            cur.execute("""
                UPDATE phone SET phone=%s 
                    WHERE id=%s;
                    """, (phones, phone_id,))
        conn.commit()


def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id FROM phone p 
                WHERE p.phone = %s;
                """, (phone,))
        phone_id = cur.fetchone()[0]
        cur.execute("""
            DELETE FROM clients_phone 
                WHERE client_id=%s AND phone_id=%s;
            """, (client_id, phone_id,))
        cur.execute("""
            DELETE FROM phone 
                WHERE id=%s;
            """, (phone_id,))
        conn.commit()


def delete_client(conn, client_id):
    pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


conn = psycopg.connect(dbname='Clients', user='postgres', password='postgres')


conn.close()
