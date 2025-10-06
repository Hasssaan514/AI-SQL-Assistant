# create_sample_db.py
import sqlite3

def create_and_seed(db_path="sample.db"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS orders;

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT,
        city TEXT
    );

    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount REAL,
        order_date TEXT,
        status TEXT,
        FOREIGN KEY(customer_id) REFERENCES customers(id)
    );

    INSERT INTO customers (name, email, city) VALUES
      ('Alice Johnson','alice@example.com','Lahore'),
      ('Bob Malik','bob@example.com','Karachi'),
      ('Charlie Khan','charlie@example.com','Islamabad');

    INSERT INTO orders (customer_id, amount, order_date, status) VALUES
      (1, 120.50, '2023-01-15', 'completed'),
      (2, 25.00, '2023-03-22', 'completed'),
      (1, 300.99, '2023-07-01', 'completed'),
      (3, 75.20, '2022-11-05', 'refunded'),
      (2, 450.00, '2023-12-10', 'completed');
    """)

    conn.commit()
    conn.close()
    print(f"Created and seeded {db_path}")

if __name__ == "__main__":
    create_and_seed()
