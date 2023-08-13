import os
import pandas as pd

from sqlalchemy import create_engine, URL, text
from flask import Flask, jsonify

DB_SERVER = os.environ.get('DB_SERVER')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_DB = os.environ.get('DB_DB')
DB_PORT = os.environ.get('DB_PORT')

#create connection URL
conn_url = URL.create("mssql+pyodbc",
                      username=DB_USER,
                      password=DB_PASS,
                      host=DB_SERVER,
                      port=DB_PORT,
                      database=DB_DB,
                      query={
                          'driver': 'ODBC DRIVER 18 for SQL Server',
                          'TrustServerCertifcate': 'yes',
                          'authentication': 'ActiveDirectoryPassword'
                      })

#create SQLAlchemy Engine
engine = create_engine(conn_url)

def get_songs(query):
    query = query.replace('\'', '\'\'')
    query = query.replace('--', '')
    query = query.replace(';', '')
    query_str = text('SELECT TOP 20 id, name, artists FROM Songs WHERE name LIKE %s%s%s' % ('\'%',query,'%\'',))

    data = pd.read_sql(query_str, engine)
    return data.to_dict(orient='records')

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_home():
    return jsonify("Hello!")

@app.route('/search/<string:query>', methods=['GET'])
def get_song_names(query):
    return jsonify(get_songs(query))

if __name__ == '__main__':
    app.run(host='0.0.0.0')