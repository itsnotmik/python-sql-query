from flask import Flask, jsonify
import pyodbc
import os
import pandas as pd

DB_SERVER = os.environ.get('DB_SERVER')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_DB = os.environ.get('DB_DB')

db_conn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"
                         "Server=" + DB_SERVER +
                         ";Database=" + DB_DB + 
                         ";Uid=" + DB_USER +
                         ";Pwd=" + DB_PASS +
                         ";Encrypt=yes;" 
                         "TrustServerCertificate=no;" 
                         "Connection Timeout=30;" 
                         "Authentication=ActiveDirectoryPassword")

def get_songs(query):
    query_str = 'SELECT TOP 20 id, name, artists FROM music_data WHERE name LIKE \'%' + query + '%\''
    data = pd.read_sql(query_str, db_conn)
    return data.to_json(orient='index')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    return jsonify("Hello!")

@app.route('/search/<string:query>', methods=['GET'])
def get_song_names(query):
    return get_songs(query)

if __name__ == '__main__':
    app.run(host='0.0.0.0')