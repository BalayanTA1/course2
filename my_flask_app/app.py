from flask import Flask, render_template, request, redirect, url_for, make_response
from db.student import add_student, get_students, delete_student, get_student_profile, authenticate_user
from db.teacher import add_teacher, get_teachers, delete_teacher, get_teacher_profile
from db.study_group import add_study_group, get_study_group_numbers, delete_study_group
from db.subject import add_subject, get_subject_name, delete_subject
from db.work_groups import get_works, delete_work_from_group
from db.work import get_student_tasks
app = Flask(__name__)


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


# Роут для профиля студента
@app.route('/profile')
def student_profile():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if user_id and user_type == 'student':
        student = get_student_profile(user_id)
        if student:
            return render_template('profile.html', student=student)
    return redirect(url_for('login_page'))

# Роут для профиля преподавателя
@app.route('/profile2')
def teacher_profile():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if user_id and user_type == 'teacher':
        teacher = get_teacher_profile(user_id)
        if teacher:
            return render_template('profile2.html', teacher=teacher)
    return redirect(url_for('login_page'))

@app.route('/tasks')
def tasks():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if user_id and user_type == 'student':
        student_tasks = get_student_tasks(user_id)
        return render_template('tasks.html', student_tasks=student_tasks)
    return redirect(url_for('login_page'))


# Роут для отображения страницы входа
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Роут для обработки авторизации
@app.route('/login', methods=['POST'])
def login():
    login = request.form.get("login")
    password = request.form.get("password")

    user_data, user_type, is_admin = authenticate_user(login, password)

    if user_data and user_type == 'student':
        response = make_response(redirect(url_for('student_profile')))
        response.set_cookie('user_id', str(user_data['student_id']))  # Устанавливаем куку с ID студента
        response.set_cookie('user_type', 'student')  # Указываем тип пользователя
        return response

    elif user_data and user_type == 'teacher':
        response = make_response(redirect(url_for('teacher_profile')))
        response.set_cookie('user_id', str(user_data['teacher_id']))  # Устанавливаем куку с ID преподавателя
        response.set_cookie('user_type', 'teacher')  # Указываем тип пользователя
        if is_admin:
            response.set_cookie('is_admin', 'true')  # Устанавливаем куку для админа
        return response

    return render_template('login.html', error="Неверный логин или пароль")


# ВСЁ РАБОТАЕТ!!!
@app.route('/admin_panel', methods=['GET'])
def admin_panel():
    # Проверяем, является ли пользователь админом
    is_admin = request.cookies.get('is_admin') == 'true'
    if not is_admin:
        return "Доступ запрещен", 403  # Возвращаем ошибку доступа
    user_type = request.args.get('user_type', 'student')
    groups = get_study_group_numbers()
    subjects = get_subject_name()
    students = get_students()
    teachers = get_teachers()
    works = get_works()
    users = students + teachers
    
    return render_template('admin_panel.html', admin_data={'groups': groups, 'users': users, 'subjects': subjects, 'works': works}, user_type=user_type)

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
    title = request.form.get('title')
    position = request.form.get('position')
    institute_id = request.form.get('institute_id')
    password = request.form.get('password')
    login = request.form.get('login')

    if full_name and position and institute_id and password and login:
        add_teacher(full_name, academic_degree, title, position, institute_id, password, login)
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

# Роут для удаления работ из групп
@app.route('/delete_work', methods=['POST'])
def delete_work():
    work_number = request.form.get('work_number')
    group_number = request.form.get('group_number')
    delete_work_from_group(work_number, group_number)
    return redirect(url_for('admin_panel'))

# Роут для выхода из системы
@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login_page')))
    response.set_cookie('user_id', '', expires=0)  # Удаляем куку с ID пользователя
    response.set_cookie('user_type', '', expires=0)  # Удаляем куку с типом пользователя
    response.set_cookie('is_admin', '', expires=0)  # Удаляем куку для админа
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

