# from flask import Flask, render_template, request, jsonify, redirect, url_for
# import psycopg2
# from psycopg2.extras import RealDictCursor

# app = Flask(__name__)

# # Настройки подключения к PostgreSQL
# DATABASE_CONFIG = {
#     'host': 'localhost',
#     'database': '123',
#     'user': '123',
#     'password': '123'
# }

# def get_db_connection():
#     conn = psycopg2.connect(**DATABASE_CONFIG)
#     return conn

# @app.route('/login2', methods=['GET', 'POST'])
# def login2():
#     if request.method == 'POST':
#         data = request.get_json()
#         login = data.get('login2')
#         password = data.get('password')

#         conn = get_db_connection()
#         cur = conn.cursor(cursor_factory=RealDictCursor)

#         # Проверка в таблице student
#         cur.execute('SELECT * FROM student WHERE login = %s AND password = %s', (login, password))
#         student = cur.fetchone()

#         if student:
#             cur.close()
#             conn.close()
#             return jsonify({'success': True, 'redirect_url': '/profile'})

#         # Проверка в таблице teacher
#         cur.execute('SELECT * FROM teacher WHERE login = %s AND password = %s', (login, password))
#         teacher = cur.fetchone()

#         if teacher:
#             cur.close()
#             conn.close()
#             return jsonify({'success': True, 'redirect_url': '/profile2'})

#         cur.close()
#         conn.close()
#         return jsonify({'success': False, 'message': 'Неверный логин или пароль'})

#     return render_template('login.html')

# # Остальные маршруты...

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)