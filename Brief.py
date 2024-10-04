import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect('factures.db')
cursor = conn.cursor()

# Supprimer les tables existantes pour réinitialiser la base de données
cursor.execute('DROP TABLE IF EXISTS Clients')
cursor.execute('DROP TABLE IF EXISTS Commandes')

# Création de la table Clients
cursor.execute('''
    CREATE TABLE IF NOT EXISTS "Client" (
        "Client_id" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Prénom" VARCHAR NOT NULL,
        "Nom" VARCHAR NOT NULL,
        "Email" VARCHAR UNIQUE NOT NULL,
        "Téléphone" VARCHAR,
        "Date_Naissance" DATE,
        "Adresse" VARCHAR NOT NULL,
        "Consentement_Marketing" INTEGER NOT NULL
    )
''')

# Création de la table Commandes
cursor.execute('''
CREATE TABLE IF NOT EXISTS "Commandes" (
    "Commande_ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Date_Commande" DATE NOT NULL,
    "Montant_Commande" INTEGER NOT NULL,
    "Client_ID" INTEGER NOT NULL,
    FOREIGN KEY ("Client_ID") REFERENCES "Client"("Client_id")
    )
''')

# Lecture du fichier CSV des clients
df_clients = pd.read_csv('jeuclients.csv')

# Insertion des données dans la table Client
for index, row in df_clients.iterrows():
    cursor.execute('''
        INSERT INTO Client (Prénom, Nom, Email, Téléphone, Date_Naissance, Adresse, Consentement_Marketing)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        row['Prénom'],
        row['Nom'],
        row['Email'],
        row['Téléphone'],
        row['Date_Naissance'],
        row['Adresse'],
        int(row['Consentement_Marketing'])  # 0 ou 1 pour le consentement marketing
    ))

# Lecture du fichier CSV des commandes
df_commandes = pd.read_csv('jeucommandes.csv')

# Insertion des données dans la table Commandes
for index, row in df_commandes.iterrows():
    cursor.execute('''
        INSERT INTO Commandes (Client_ID, Date_Commande, Montant_Commande)
        VALUES (?, ?, ?)
    ''', (
        row['Client_ID'],
        row['Date_Commande'],
        row['Montant_Commande']
    ))

# Commit les modifications après toutes les insertions
conn.commit()

print('Tous les clients consentant:')
cursor.execute('SELECT * from Client WHERE Consentement_Marketing = 1')
clients = cursor.fetchall()

# Affichage des résultats
for client in clients:
    print(client)
print('--------------------')

print('Toutes les commandes de l id client 56:')
cursor.execute('SELECT * from Commandes WHERE Client_ID = 56')
clients = cursor.fetchall()

# Affichage des résultats
for client in clients:
    print(client)
print('--------------------')

print('Somme du client 61:')
cursor.execute('SELECT SUM(Montant_Commande) FROM Commandes WHERE Client_ID = 61')
clients = cursor.fetchall()

# Affichage des résultats
for client in clients:
    print(client)
print('--------------------')

print('Les clients avec une somme supérieure à 100:')
cursor.execute('''
SELECT Client_ID 
FROM Commandes 
GROUP BY Client_ID
HAVING SUM(Montant_Commande) > 100;
''')
clients = cursor.fetchall()

# Affichage des résultats
for client in clients:
    print(client)
print('--------------------')

print('Les clients ayant passé des commandes après le 01/01/2023:')
cursor.execute('''
SELECT DISTINCT Client_ID 
FROM Commandes 
WHERE Date_Commande > '2023-01-01'
ORDER BY Client_ID ASC;
''')
clients = cursor.fetchall()

# Affichage des résultats
for client in clients:
    print(client)
print('--------------------')

# Fermer la connexion
conn.close()
