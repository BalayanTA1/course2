# from flask import Flask, render_template, request, redirect, url_for

# app = Flask(__name__)

# # Данные о студенте
# student_data = {
#     'student_id': '123456',
#     'full_name': 'Иванов Иван Иванович',
#     'specialty': 'Информатика',
#     'education_form': 'Очная',
#     'group_number': 'ИУ-101',
#     'email': 'ivanov@example.com',
#     'phone': '+7 (999) 123-45-67'
# }

# # Данные о преподавателях
# teacher_data = {
#     'full_name': 'Иванов Иван Иванович',
#     'subjects': 'Информатика',
#     'position': 'Ст.Преподаватель',
#     'academic_degree': 'Доктор наук',
#     'title': '??',
#     'institute_number': '7',
#     'email': 'ivanov@example.com',
#     'phone': '+7 (999) 123-45-67'
# }

# # Данные о заданиях студента
# student_tasks = [
#     {
#         'name': 'Математика',
#         'number': '101',
#         'title': 'Алгебра',
#         'status': 'active',
#         'points': '90',
#         'type': 'Основной',
#         'date': '6/10/2020'
#     },
#     {
#         'name': 'Физика',
#         'number': '102',
#         'title': 'Механика',
#         'status': 'inactive',
#         'points': '75',
#         'type': 'Дополнительный',
#         'date': '6/10/2020'
#     }
# ]

# # Данные для админ панели
# admin_data = {
#     'users': [
#         {'full_name': 'Иванов Иван Иванович', 'type': 'Студент'},
#         {'full_name': 'Петрова Мария Сергеевна', 'type': 'Преподаватель'},
#     ],
#     'groups': [
#         {'name': 'Группа 2443'},
#         {'name': 'Группа 1796'},
#     ],
#     'subjects': [
#         {'name': 'Математика'},
#         {'name': 'Физика'},
#     ],
#     'tasks': [
#         {'type': 'Контрольная', 'name': 'Математика', 'deadline': '2024-01-15'},
#         {'type': 'Лабораторная', 'name': 'Физика', 'deadline': '2024-02-20'},
#     ]
# }

# # Маршруты для страниц
# @app.route('/')
# def profile():
#     return render_template('profile.html', student=student_data)

# @app.route('/profile2')
# def profile2():
#     return render_template('profile2.html', teacher=teacher_data)

# # Маршрут для отображения страницы заданий
# @app.route('/tasks')
# def tasks():
#     return render_template('tasks.html', student_tasks=student_tasks)

# # Маршрут для отображения админ-панели
# @app.route('/admin_panel')
# def admin_panel():
#     return render_template('admin_panel.html', admin_data=admin_data)

# @app.route('/login')
# def login():
#     return render_template('login.html')




# @app.route('/test', methods=['POST'])
# def test():
#     login = request.form.get("login")
#     password = request.form.get("password")
#     print(login, password)
#     return render_template('admin_panel.html', admin_data=admin_data)

# @app.route('/add_user', methods=['POST'])
# def add_user():
#     user_type = request.form.get("user_type")
#     full_name = request.form.get("full_name")
#     email = request.form.get("email")
#     phone = request.form.get("phone")
    
#     # Здесь можно добавить логику для сохранения пользователя в базу данных
#     print(f"Добавлен пользователь: {full_name}, {email}, {phone}, {user_type}")
    
#     return redirect(url_for('admin_panel'))

# @app.route('/add_group', methods=['POST'])
# def add_group():
#     group_name = request.form.get("group_name")
    
#     # Здесь можно добавить логику для сохранения группы в базу данных
#     print(f"Добавлена группа: {group_name}")
    
#     return redirect(url_for('admin_panel'))

# @app.route('/add_subject', methods=['POST'])
# def add_subject():
#     subject_name = request.form.get("subject_name")
    
#     # Здесь можно добавить логику для сохранения предмета в базу данных
#     print(f"Добавлен предмет: {subject_name}")
    
#     return redirect(url_for('admin_panel'))

# @app.route('/add_task', methods=['POST'])
# def add_task():
#     task_type = request.form.get("task_type")
#     task_name = request.form.get("task_name")
#     deadline = request.form.get("deadline")
    
#     # Здесь можно добавить логику для сохранения задачи в базу данных
#     print(f"Добавлена задача: {task_name}, {task_type}, {deadline}")
    
#     return redirect(url_for('admin_panel'))