import sqlite3
from models import Client

def connect():
    """Connect to the SQLite database and create the client table if it doesn't exist."""
    conn = sqlite3.connect("Clients.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS client (
                    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    gender TEXT,
                    phone TEXT,
                    address TEXT
                )""")
    conn.commit()
    conn.close()

# Initial client data
client_data = [
    {
        'name': 'Adama',
        'gender': 'Masculin',
        'phone': '123456789',
        'address': 'Scat',
    },
]

def insert(client):
    """Insert a new client into the database."""
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO client (name, gender, phone, address) VALUES (?, ?, ?, ?)", (
        client.name,
        client.gender,
        client.phone,
        client.address
    ))
    conn.commit()
    conn.close()

def initialize_database():
    """Connect to the database, create the table, and insert initial data."""
    connect()

    # Insert initial clients if the table is empty
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM client")
    count = cur.fetchone()[0]
    conn.close()

    if count == 0:  # Check if the table is empty before inserting
        for data in client_data:
            cl = Client(data['name'], data['gender'], data['phone'], data['address'])
            insert(cl)

if __name__ == '__main__':
    initialize_database()
