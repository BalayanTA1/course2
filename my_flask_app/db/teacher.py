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