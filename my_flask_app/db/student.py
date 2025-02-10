from db.db import execute_query

def print_students():
    query = "SELECT * FROM Student;"
    students = execute_query(query)
    print("\nСтуденты:")
    for student in students:
        print(student)

def add_student(full_name, education_form, group_number, password, login):
    query = "INSERT INTO Student (full_name, education_form, group_number, password, login) VALUES (%s, %s, %s, %s, %s) RETURNING student_id;"
    result = execute_query(query, (full_name, education_form, group_number, password, login))
    if result:
        print(f"Добавлен студент с ID: {result[0]['student_id']}")

def delete_student(student_id):
    query = "DELETE FROM Student WHERE student_id = %s RETURNING student_id;"
    result = execute_query(query, (student_id,))
    if result:
        print(f"Удален студент с ID: {result[0]['student_id']}")

def get_student(student_id):
    query = "SELECT * FROM Student WHERE student_id = %s;"
    student = execute_query(query, (student_id,))
    result = student[0] if student else None
    print(result)  
    return result

def get_students():
    query = "SELECT student_id AS id, full_name, 'Студент' AS type FROM Student"
    students = execute_query(query)
    return students

def get_student_profile(student_id):
    student_query = "SELECT * FROM Student WHERE student_id = %s"
    student = execute_query(student_query, (student_id,), fetch=True)
    return student[0] if student else None

# Проверяет, существует ли пользователь в таблицах Student или Teacher.
# Возвращает данные пользователя и его тип (student или teacher).
def authenticate_user(login, password):
    student_query = "SELECT * FROM Student WHERE login = %s AND password = %s"
    student = execute_query(student_query, (login, password), fetch=True)

    if student:
        return student[0], 'student'

    teacher_query = "SELECT * FROM Teacher WHERE login = %s AND password = %s"
    teacher = execute_query(teacher_query, (login, password), fetch=True)

    if teacher:
        is_admin = teacher[0]['is_admin']  # Проверяем, является ли преподаватель админом
        return teacher[0], 'teacher', is_admin

    return None, None, False