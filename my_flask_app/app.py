from flask import Flask, render_template, request, redirect, url_for
from db.student import add_student, get_students, delete_student
from db.teacher import add_teacher, get_teachers, delete_teacher
from db.study_group import add_study_group, get_study_group_numbers, delete_study_group
from db.subject import add_subject, get_subject_name, delete_subject_route
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
    'tasks': [
        {'type': 'Контрольная', 'name': 'Математика', 'deadline': '2024-01-15'},
        {'type': 'Лабораторная', 'name': 'Физика', 'deadline': '2024-02-20'},
    ]
}

# Маршруты для страниц
@app.route('/profile')
def profile():
    return render_template('profile.html', student=student_data)

@app.route('/profile2')
def profile2():
    return render_template('profile2.html', teacher=teacher_data)

@app.route('/tasks')
def tasks():
    return render_template('tasks.html', student_tasks=student_tasks)


@app.route('/login')
def login():
    return render_template('login.html')

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
@app.route('/admin_panel', methods=['GET'])
def admin_panel():
    user_type = request.args.get('user_type', 'student')
    groups = get_study_group_numbers()
    subjects = get_subject_name()
    
    students = get_students()
    teachers = get_teachers()
    
    users = students + teachers
    
    return render_template('admin_panel.html', admin_data={'groups': groups, 'users': users, 'subjects': subjects, 'tasks': admin_data['tasks']}, user_type=user_type)

# Маршрут для обработки добавления группы
@app.route('/add_group', methods=['POST'])
def add_group():
    institute_id = request.form.get('institute_id')
    if institute_id:
        add_study_group(institute_id)
    return redirect(url_for('admin_panel')) 

@app.route('/delete_group', methods=['POST'])
def delete_group():
    group_number = request.form.get('group_number')
    delete_study_group(group_number)
    return redirect(url_for('admin_panel'))


# Маршрут для обработки добавления предмета
@app.route('/add_subject', methods=['POST'])
def add_subject_route():
    name = request.form.get('name')  
    if name:
        add_subject(name)  
    return redirect(url_for('admin_panel'))  

@app.route('/delete_subject', methods=['POST'])
def delete_subject_route():
    subject_name = request.form.get('subject_name')  
    delete_subject(subject_name)  
    return redirect(url_for('admin_panel'))



# Маршрут для обработки добавления студента
@app.route('/add_student', methods=['POST'])
def add_student_route():
    full_name = request.form.get('full_name')
    education_form = request.form.get('education_form')
    group_number = request.form.get('group_number')
    password = request.form.get('password')
    login = request.form.get('login')

    if full_name and education_form and group_number and password and login:
        add_student(full_name, education_form, group_number, password, login)
    return redirect(url_for('admin_panel'))

# Маршрут для обработки добавления преподавателя
@app.route('/add_teacher', methods=['POST'])
def add_teacher_route():
    full_name = request.form.get('full_name')
    academic_degree = request.form.get('academic_degree')
    position = request.form.get('position')
    institute_id = request.form.get('institute_id')
    password = request.form.get('password')
    login = request.form.get('login')

    if full_name and position and institute_id and password and login:
        add_teacher(full_name, academic_degree, None, position, institute_id, password, login)
    return redirect(url_for('admin_panel'))

@app.route('/delete_user', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')  
    user_type = request.form.get('user_type')  

    if user_type == 'Студент':
        delete_student(user_id)
    elif user_type == 'Преподаватель':
        delete_teacher(user_id)

    return redirect(url_for('admin_panel'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

