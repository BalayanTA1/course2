import os
from datetime import datetime
from flask import send_from_directory
from db.db import execute_query
from db.uploaded_files import insert_uploaded_file
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from db.student import add_student, get_students, delete_student, get_student_profile, authenticate_user
from db.teacher import add_teacher, get_teachers, delete_teacher, get_teacher_profile, get_teacher_works
from db.study_group import add_study_group, get_study_group_numbers, delete_study_group
from db.subject import add_subject, get_subject_name, delete_subject
from db.work_groups import get_works, delete_work_from_group
from db.work import get_student_tasks
from db.work_result import insert_grade, update_grade, check_existing_grade
app = Flask(__name__)

# Настройки для загрузки файлов
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')  # Папка для загрузки
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # Ограничение на размер файла (2 МБ)
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}  # Разрешенные расширения файлов

# Создаем папку для загрузки, если она не существует
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Функция для проверки расширения файла
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Роут для загрузки PDF
@app.route('/upload', methods=['POST'])
def upload_file():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if not user_id or user_type != 'student':  # Проверяем, авторизован ли студент
        return redirect(url_for('login_page'))

    if 'file' not in request.files:
        flash('Файл не выбран', 'error')
        return redirect(url_for('tasks'))  # Перенаправляем на страницу заданий

    file = request.files['file']

    if file.filename == '':
        flash('Файл не выбран', 'error')
        return redirect(url_for('tasks'))  # Перенаправляем на страницу заданий

    if file and allowed_file(file.filename):
        if file.content_length > app.config['MAX_CONTENT_LENGTH']:
            flash('Файл слишком большой. Максимальный размер — 2 МБ.', 'error')
            return redirect(url_for('tasks'))  # Перенаправляем на страницу заданий

        # Сохранение файла с уникальным именем
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Получаем номер работы из формы
        work_number = request.form.get('work_number')

        # Сохраняем информацию о файле в базу данных
        try:
            # Вставляем запись и получаем время загрузки
            upload_date = insert_uploaded_file(user_id, work_number, file_path)
            flash('Файл успешно загружен', 'success')
            # Передаем work_number и upload_date в параметрах URL
            return redirect(url_for('tasks', work_number=work_number, upload_date=upload_date))
        except Exception as e:
            flash(f'Ошибка при загрузке файла: {str(e)}', 'error')

        return redirect(url_for('tasks'))  # Перенаправляем на страницу заданий

    flash('Недопустимый формат файла. Разрешены только PDF.', 'error')
    return redirect(url_for('tasks'))  # Перенаправляем на страницу заданий



def insert_uploaded_file(student_id, work_number, file_path):
    query = "INSERT INTO Uploaded_Files (student_id, work_number, file_path) VALUES (%s, %s, %s) RETURNING upload_date"
    params = (student_id, work_number, file_path)
    result = execute_query(query, params, fetch=True)
    return result[0]['upload_date']  # Возвращаем время загрузки



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
        work_number = request.args.get('work_number')  # Получаем work_number из параметров URL
        upload_date = request.args.get('upload_date')  # Получаем upload_date из параметров URL
        return render_template('tasks.html', student_tasks=student_tasks, work_number=work_number, upload_date=upload_date)
    return redirect(url_for('login_page'))



@app.route('/teacher_tasks')
def teacher_tasks():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if user_id and user_type == 'teacher':
        # Получаем загруженные файлы, относящиеся к предметам преподавателя
        query = """
            SELECT uf.file_id, uf.student_id, s.full_name AS student_name, 
                   uf.work_number, w.name AS work_name, uf.file_path, uf.upload_date
            FROM Uploaded_Files uf
            JOIN Work w ON uf.work_number = w.work_number
            JOIN Student s ON uf.student_id = s.student_id
            JOIN Teacher_Subject ts ON w.subject_name = ts.subject_name
            WHERE ts.teacher_id = %s
        """
        uploaded_files = execute_query(query, (user_id,))
        return render_template('tasks2.html', uploaded_files=uploaded_files)
    return redirect(url_for('login_page'))

#Роут для скачивания файла
@app.route('/download/<int:file_id>')
def download_file(file_id):
    # Получаем путь к файлу из базы данных
    query = "SELECT file_path FROM Uploaded_Files WHERE file_id = %s"
    result = execute_query(query, (file_id,))
    if result:
        file_path = result[0]['file_path']
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        return send_from_directory(directory, filename, as_attachment=True)
    flash('Файл не найден', 'error')
    return redirect(url_for('teacher_tasks'))

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
        response.set_cookie('user_id', str(user_data['student_id']))  # Устанавливаем cookie с ID студента
        response.set_cookie('user_type', 'student')  # Указываем тип пользователя
        return response

    elif user_data and user_type == 'teacher':
        response = make_response(redirect(url_for('teacher_profile')))
        response.set_cookie('user_id', str(user_data['teacher_id']))  # Устанавливаем cookie с ID преподавателя
        response.set_cookie('user_type', 'teacher')  # Указываем тип пользователя
        if is_admin:
            response.set_cookie('is_admin', 'true')  # Устанавливаем cookie для админа
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

# Роут для добавления группы
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


# Роут для добавления предмета
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



# Роут для добавления студента
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

# Роут для добавления преподавателя
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

# Роут для назначения работы группе
@app.route('/add_work_to_group', methods=['POST'])
def add_work_to_group():
    date = request.form.get('date')
    deadline = request.form.get('deadline')
    group_number = request.form.get('group_number')
    work_number = request.form.get('work_number')
    subject_name = request.form.get('subject_name')

    query = """
        INSERT INTO Work_Groups (date, deadline, group_number, work_number, subject_name)
        VALUES (%s, %s, %s, %s, %s)
    """
    params = (date, deadline, group_number, work_number, subject_name)
    execute_query(query, params)

    return redirect(url_for('admin_panel'))

# Роут для удаления назначеных работ
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
    response.set_cookie('user_id', '', expires=0)  # Удаляем cookie с ID пользователя
    response.set_cookie('user_type', '', expires=0)  # Удаляем cookie с типом пользователя
    response.set_cookie('is_admin', '', expires=0)  # Удаляем cookie для админа
    response.set_cookie('session', '', expires=0)  # Откуда они?
    return response

@app.route('/grade_work', methods=['POST'])
def grade_work():
    user_id = request.cookies.get('user_id')
    user_type = request.cookies.get('user_type')

    if user_id and user_type == 'teacher':
        student_id = request.form.get('student_id')
        work_number = request.form.get('work_number')
        grade = request.form.get('grade')
        submission_date = datetime.now().date()

        # Проверяем, существует ли уже запись в таблице Work_Result
        existing_grade = check_existing_grade(student_id, work_number)

        if existing_grade:
            # Обновляем существующую оценку
            update_grade(student_id, work_number, grade, submission_date)
        else:
            # Вставляем новую оценку
            insert_grade(student_id, work_number, grade, submission_date)

        flash('Оценка успешно сохранена', 'success')
    else:
        flash('Ошибка: вы не авторизованы как преподаватель', 'error')

    return redirect(url_for('teacher_tasks'))

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'  # Ключ для работы с flash-сообщениями
    app.run(host='0.0.0.0', port=8000)

