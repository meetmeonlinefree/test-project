from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = 'database.db'

# Создание таблицы с новыми полями
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS drivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return 'API работает. Используй POST /register для регистрации водителя.'

# ✅ Регистрация водителя
@app.route('/register', methods=['POST'])
def register_driver():
    data = request.get_json()
    name = data.get('name')
    phone = data.get('phone')
    password = data.get('password')

    if not name or not phone or not password:
        return jsonify({'status': 'error', 'message': 'Name, phone, and password are required'}), 400

    created_at = updated_at = datetime.utcnow().isoformat()

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO drivers (name, phone, password, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, password, created_at, updated_at))
        conn.commit()
        conn.close()
        return jsonify({'status': 'success', 'message': 'Driver registered successfully'})
    except sqlite3.IntegrityError:
        return jsonify({'status': 'error', 'message': 'Phone already registered'}), 409

# ✅ Получить всех водителей
@app.route('/drivers', methods=['GET'])
def get_all_drivers():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, created_at, updated_at FROM drivers')
    drivers = cursor.fetchall()
    conn.close()

    result = []
    for d in drivers:
        result.append({
            'id': d[0],
            'name': d[1],
            'phone': d[2],
            'created_at': d[3],
            'updated_at': d[4],
        })

    return jsonify(result)

# ✅ Получить одного водителя по ID
@app.route('/drivers/<int:driver_id>', methods=['GET'])
def get_driver_by_id(driver_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, phone, created_at, updated_at FROM drivers WHERE id = ?', (driver_id,))
    driver = cursor.fetchone()
    conn.close()

    if driver:
        return jsonify({
            'id': driver[0],
            'name': driver[1],
            'phone': driver[2],
            'created_at': driver[3],
            'updated_at': driver[4],
        })
    else:
        return jsonify({'status': 'error', 'message': 'Driver not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
