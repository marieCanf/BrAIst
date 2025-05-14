"""
Avant d'utiliser le script, vérifiez que vous disposez de la bibliothèque "mysql-connector-python" installé
Si ce n'est pas le cas, installez le avec la commande suivante:
    pip install mysql-connector-python
"""


from database import get_connection


conn = get_connection()

cursor = conn.cursor()

sql_script = """
CREATE TABLE IF NOT EXISTS Utilisateur (
    INAMI INT PRIMARY KEY,
    Adresse_mail VARCHAR(255) NOT NULL,
    Nom VARCHAR(255) NOT NULL,
    Prenom VARCHAR(255) NOT NULL,
    Mot_de_passe VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Patient (
    NISS VARCHAR(11) PRIMARY KEY,
    Nom VARCHAR(255),
    Prenom VARCHAR(255),
    Resultat_suivi INT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS IRM (
    Id_irm INT PRIMARY KEY AUTO_INCREMENT,
    Lien_irm TEXT,
    NISS VARCHAR(11),
    INAMI INT,
    FOREIGN KEY (NISS) REFERENCES Patient(NISS),  
    FOREIGN KEY (INAMI) REFERENCES Utilisateur(INAMI)
);

CREATE TABLE IF NOT EXISTS Discussion (
    Id_discussion INT PRIMARY KEY AUTO_INCREMENT,
    Contenu_discussion TEXT,
    NISS VARCHAR(11),
    FOREIGN KEY (NISS) REFERENCES Patient(NISS)
);

CREATE TABLE IF NOT EXISTS Caracteristiques_IRM (
    Id_caracteristique INT PRIMARY KEY AUTO_INCREMENT,
    Id_irm INT,
    NISS VARCHAR(11),
    Date_extraction DATETIME,
    Chemin_csv TEXT,
    Statut_traitement VARCHAR(50) DEFAULT 'En attente',
    FOREIGN KEY (Id_irm) REFERENCES IRM(Id_irm),
    FOREIGN KEY (NISS) REFERENCES Patient(NISS)
);
CREATE TABLE IF NOT EXISTS Caracteristiques_IRM (
    Id_caracteristique INT PRIMARY KEY AUTO_INCREMENT,
    Id_irm INT NULL,
    NISS VARCHAR(11),
    Date_extraction DATETIME,
    Chemin_csv TEXT,
    Statut_traitement VARCHAR(50) DEFAULT 'En attente',
    FOREIGN KEY (Id_irm) REFERENCES IRM(Id_irm),
    FOREIGN KEY (NISS) REFERENCES Patient(NISS)
);
"""
try :
    for statement in sql_script.split(";"):
        if statement.strip():
            cursor.execute(statement)

    conn.commit()
finally :
    cursor.close()
    conn.close()

print("Database and tables created successfully!")