import mysql.connector

def get_connection():
    return mysql.connector.connect(
    host="212.83.130.244",
    user="deepilia",
    password="fMFh_kdzMQpsdgC2VQ",
    database="deepilia"
)