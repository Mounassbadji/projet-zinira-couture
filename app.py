from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Classe Client
class Client:
    def __init__(self, client_id, name, gender, phone, address):
        self.client_id = client_id
        self.name = name
        self.gender = gender
        self.phone = phone
        self.address = address

# Fonction pour connecter à la base de données
def connect():
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

# Fonction pour insérer un client
def insert(client):
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO client (name, gender, phone, address) VALUES (?, ?, ?, ?)", (
        client.name,
        client.gender,
        client.phone,
        client.address,
    ))
    conn.commit()
    conn.close()

# Fonction pour récupérer les clients
def view():
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM client")
    rows = cur.fetchall()
    clients = [Client(row[0], row[1], row[2], row[3]) for row in rows]  
    conn.close()
    return clients

# Fonction pour mettre à jour un client
def update(client):
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("UPDATE client SET name=?, gender=?, phone=?, address=? WHERE client_id=?", (
        client.name,
        client.gender,
        client.phone,
        client.address,
        client.client_id
    ))
    conn.commit()
    conn.close()

# Fonction pour supprimer un client
def delete(client_id):
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM client WHERE client_id=?", (client_id,))
    conn.commit()
    conn.close()

# Route pour afficher les clients
@app.route('/index')
def index():
    clients = view()  # Récupération de la liste des clients
    return render_template('index.html', clients=clients)

# Route pour modifier un client
@app.route('/modifier_client/<int:client_id>', methods=['GET', 'POST'])
def modifier_client(client_id):
    if request.method == 'POST':
        client = Client(
            client_id=client_id,
            name=request.form.get('name'),
            gender=request.form.get('gender'),
            phone=request.form.get('phone'),
            address=request.form.get('address')
        )
        update(client)  # Mise à jour dans la base de données
        flash('Client modifié avec succès!')
        return redirect(url_for('index'))

    # Récupération des détails du client pour le formulaire
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM client WHERE client_id=?", (client_id,))
    row = cur.fetchone()
    conn.close()

    client = Client(row[0], row[1], row[2], row[3], row[4]) if row else None

    return render_template('modifier_client.html', client=client)

# Route pour supprimer un client
@app.route('/delete_client/<int:client_id>', methods=['GET', 'POST'])
def delete_client(client_id):
    conn = sqlite3.connect('Clients.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM client WHERE client_id=?", (client_id,))
    row = cur.fetchone()
    client = Client(row[0], row[1], row[2], row[3], row[4]) if row else None
    conn.close()

    if request.method == 'POST':
        if client:
            delete(client_id) 
            flash('Client supprimé avec succès!')
            return redirect(url_for('index'))
        else:
            flash('Client non trouvé.')

    return render_template('delete_client.html', client=client)

if __name__ == '__main__':
    connect()  
    app.run(debug=True)
