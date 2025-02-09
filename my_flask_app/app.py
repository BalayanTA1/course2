from flask import Flask, render_template, request, redirect, url_for
# from db.student import add_student
# from db.teacher import add_teacher
# from db.study_group import add_study_group
from db.subject import add_subject
app = Flask(__name__)

# Данные о студенте
student_data = {
    'student_id': '123456',
    'full_name': 'Иванов Иван Иванович',
    'specialty': 'Информатика',
    'education_form': 'Очная',
    'group_number': 'ИУ-101',
    'email': 'ivanov@example.com',
    'phone': '+7 (999) 123-45-67'
}

# Данные о преподавателях
teacher_data = {
    'full_name': 'Иванов Иван Иванович',
    'subjects': 'Информатика',
    'position': 'Ст.Преподаватель',
    'academic_degree': 'Доктор наук',
    'title': '??',
    'institute_number': '7',
    'email': 'ivanov@example.com',
    'phone': '+7 (999) 123-45-67'
}

# Данные о заданиях студента
student_tasks = [
    {
        'name': 'Математика',
        'number': '101',
        'title': 'Алгебра',
        'status': 'active',
        'points': '90',
        'type': 'Основной',
        'date': '6/10/2020'
    },
    {
        'name': 'Физика',
        'number': '102',
        'title': 'Механика',
        'status': 'inactive',
        'points': '75',
        'type': 'Дополнительный',
        'date': '6/10/2020'
    }
]

# Данные для админ панели
admin_data = {
    'users': [
        {'full_name': 'Иванов Иван Иванович', 'type': 'Студент'},
        {'full_name': 'Петрова Мария Сергеевна', 'type': 'Преподаватель'},
    ],
    'groups': [
        {'name': 'Группа 2443'},
        {'name': 'Группа 1796'},
    ],
    'subjects': [
        {'name': 'Математика'},
        {'name': 'Физика'},
    ],
    'tasks': [
        {'type': 'Контрольная', 'name': 'Математика', 'deadline': '2024-01-15'},
        {'type': 'Лабораторная', 'name': 'Физика', 'deadline': '2024-02-20'},
    ]
}

# Маршруты для страниц
@app.route('/')
def profile():
    return render_template('profile.html', student=student_data)

@app.route('/profile2')
def profile2():
    return render_template('profile2.html', teacher=teacher_data)

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', student_tasks=student_tasks)

@app.route('/admin_panel')
def admin_panel():
    return render_template('admin_panel.html', admin_data=admin_data)

@app.route('/login')
def login():
    return render_template('login.html')




# @app.route('/test', methods=['POST'])
# def test():
#     login = request.form.get("login")
#     password = request.form.get("password")
#     print(login, password)
#     return render_template('admin_panel.html', admin_data=admin_data)






# @app.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     if request.method == 'POST':
#         user_type = request.form.get("user_type")
#         full_name = request.form.get("full_name")
#         password = request.form.get("password")
#         login = request.form.get("login")

#         if user_type == "student":
#             education_form = request.form.get("education_form")
#             group_number = request.form.get("group_number")
#             add_student(full_name, education_form, group_number, password, login)
#         elif user_type == "teacher":
#             academic_degree = request.form.get("academic_degree")
#             title = request.form.get("title")
#             position = request.form.get("position")
#             institute_id = request.form.get("institute_id")
#             add_teacher(full_name, academic_degree, title, position, institute_id, password, login)

#         return redirect(url_for('admin_panel'))

    # Если метод GET, передаем user_type в шаблон (по умолчанию 'student')
    # user_type = request.args.get('user_type', 'student')
    # return render_template('admin_panel.html', user_type=user_type)




# @app.route('/add_task', methods=['POST'])
# def add_task():
#     task_type = request.form.get("task_type")
#     task_name = request.form.get("task_name")
#     deadline = request.form.get("deadline")
    
#     # Здесь можно добавить логику для сохранения задачи в базу данных
#     print(f"Добавлена задача: {task_name}, {task_type}, {deadline}")
    
#     return redirect(url_for('admin_panel'))

# ВСЁ РАБОТАЕТ!!!
# Маршрут для обработки добавления группы
# @app.route('/add_group', methods=['POST'])
# def add_group():
#     institute_id = request.form.get('institute_id')
#     if institute_id:
#         add_study_group(institute_id)
#     return redirect(url_for('admin_panel')) 

# Маршрут для обработки добавления предмета
@app.route('/add_subject', methods=['POST'])
def add_subject_route():
    name = request.form.get('name')  # Получаем название предмета из формы
    if name:
        add_subject(name)  # Вызываем функцию добавления предмета
    return redirect(url_for('admin_panel'))  

if __name__ == '__main__':
    # add_student("azs", "jxyfz", "26", "123", "34erhf5345345345")
    # add_study_group(29)
    app.run(host='0.0.0.0', port=8000)

