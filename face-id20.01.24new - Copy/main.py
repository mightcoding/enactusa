from flask import Flask, render_template, request, jsonify
import base64
import os
import sqlite3

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    with sqlite3.connect('FaceBase.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS Users
                     (ID INT PRIMARY KEY NOT NULL,
                     Name TEXT NOT NULL,
                     Age INT NOT NULL,
                     Gender TEXT NOT NULL,
                     CR TEXT NOT NULL);''')

# Функция для добавления/обновления пользователя
def insert_or_update_user(id, name, age, gender, cr):
    with sqlite3.connect('FaceBase.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT OR REPLACE INTO Users (ID, Name, Age, Gender, CR)
                          VALUES (?, ?, ?, ?, ?);''', (id, name, age, gender, cr))
        conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_image', methods=['POST'])
def save_image():
    user_id = request.form['id']
    name = request.form['name']
    age = request.form['age']
    gender = request.form['gender']
    cr = request.form['cr']
    image_data = request.form['imageData']
    image_data = base64.b64decode(image_data.split(',')[1])
    
    # Добавление/обновление пользователя
    insert_or_update_user(user_id, name, age, gender, cr)
    
    # Сохранение изображения
    if not os.path.exists('static/photos'):
        os.makedirs('static/photos')
    filepath = f'static/photos/{user_id}_{len(os.listdir("static/photos"))}.png'
    with open(filepath, 'wb') as file:
        file.write(image_data)
    return jsonify({'message': 'Фотография сохранена и пользователь обновлен'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
