from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('data/venues.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/venues')
def get_venues():
    conn = get_db_connection()
    venues = conn.execute('SELECT * FROM venues').fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in venues])

if __name__ == '__main__':
    app.run(debug=True)