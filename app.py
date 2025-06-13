from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = 'database.db'

# Создание таблицы
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Endpoint регистрации водителя
@app.route('/register', methods=['POST'])
def register_driver():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')

    if not name or not phone:
        return jsonify({'status': 'error', 'message': 'Name and phone are required'}), 400

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO drivers (name, phone) VALUES (?, ?)', (name, phone))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Driver registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Phone already registered'}), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
