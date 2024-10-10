from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete'

# Simulons une base de données avec une liste
clients = [
    {'id': 1, 'name': 'TA BINTA', 'gender': 'Femme', 'phone': '', 'address': ''},
    {'id': 2, 'name': 'CHEIKH TIDIANE SARR MARRA', 'gender': 'Homme', 'phone': '', 'address': ''},
   
]

@app.route('/')
def index():
    return render_template('index.html', clients=clients)

@app.route('/add_client', methods=['POST'])
def add_client():
    name = request.form.get('name')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    address = request.form.get('address')

    if name:
        new_client = {
            'id': len(clients) + 1,
            'name': name,
            'gender': gender,
            'phone': phone,
            'address': address
        }
        clients.append(new_client)
        flash('Client ajouté avec succès!')
    else:
        flash('Erreur: Le nom est requis.')

    return redirect(url_for('index'))

@app.route('/delete_client/<int:client_id>')
def delete_client(client_id):
    global clients
    clients = [client for client in clients if client['id'] != client_id]
    flash('Client supprimé avec succès!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
