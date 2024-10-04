import sqlite3
import pandas as pd

# Connexion à la base de données
conn = sqlite3.connect('factures.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS Clients')
cursor.execute('DROP TABLE IF EXISTS Commandes')

# Création de la table Clients si elle n'existe pas
cursor.execute('''CREATE TABLE IF NOT EXISTS "Client" (
    "Client_id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "Prénom" VARCHAR NOT NULL,
    "Nom" VARCHAR NOT NULL,
    "Email" VARCHAR,
    "téléphone" VARCHAR,
    "Date_naissance" DATE NOT NULL,
    "Adresse" VARCHAR NOT NULL,
    "Consentement_Marketing" INTEGER NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS "Commandes" (
	"Commande_ID" INTEGER NOT NULL UNIQUE,
	"Date_Commande" DATE NOT NULL,
	"Montant_Commande" INTEGER NOT NULL,
	"Client_ID" INTEGER NOT NULL,
	PRIMARY KEY("Commande_ID"),
	FOREIGN KEY ("Client_ID") REFERENCES "Client"("Client_id")
	ON UPDATE NO ACTION ON DELETE NO ACTION
)''')
