from db.db import execute_query

def print_teachers():
    query = "SELECT * FROM Teacher;"
    teachers = execute_query(query)
    print("\nПреподаватели:")
    for teacher in teachers:
        print(teacher)

def add_teacher(full_name, academic_degree, title, position, institute_id, password, login):
    query = "INSERT INTO Teacher (full_name, academic_degree, title, position, institute_id, password, login) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING teacher_id;"
    result = execute_query(query, (full_name, academic_degree, title, position, institute_id, password, login))
    if result:
        print(f"Добавлен преподаватель с ID: {result[0]['teacher_id']}")

def delete_teacher(teacher_id):
    query = "DELETE FROM Teacher WHERE teacher_id = %s RETURNING teacher_id;"
    result = execute_query(query, (teacher_id,))
    if result:
        print(f"Удален преподаватель с ID: {result[0]['teacher_id']}")

def get_teacher(teacher_id):
    query = "SELECT * FROM Teacher WHERE teacher_id = %s;"
    teacher = execute_query(query, (teacher_id,))
    result = teacher[0] if teacher else None
    print(result)  
    return result

def get_teachers():
    query = "SELECT teacher_id AS id, full_name, 'Преподаватель' AS type FROM Teacher"
    teachers = execute_query(query)
    return teachers

def get_teacher_profile(teacher_id):
    teacher_query = "SELECT * FROM Teacher WHERE teacher_id = %s"
    teacher = execute_query(teacher_query, (teacher_id,), fetch=True)
    return teacher[0] if teacher else None

# UPDATE Teacher 
# SET is_admin = FALSE 
# WHERE teacher_id = 2;
def update_teacher_admin_status(teacher_id, is_admin):
    query = "UPDATE Teacher SET is_admin = %s WHERE teacher_id = %s;"
    execute_query(query, (is_admin, teacher_id))
    print(f"Статус администратора для преподавателя с ID {teacher_id} обновлен на {is_admin}.")


def get_teacher_works(teacher_id):
    # Запрос для получения всех работ, которые ведет преподаватель
    query = '''
        SELECT w.work_number, w.name, w.is_lab, w.is_control
        FROM Work w
        JOIN Teacher_Subject ts ON w.subject_name = ts.subject_name
        WHERE ts.teacher_id = %s
    '''
    works = execute_query(query, (teacher_id,), fetch=True)

    # Преобразуем данные в удобный формат
    teacher_works = []
    for work in works:
        work_type = 'Лабораторная' if work['is_lab'] else 'Контрольная'
        teacher_works.append({
            'number': work['work_number'],
            'title': work['name'],
            'type': work_type
        })

    return teacher_works