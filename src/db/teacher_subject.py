from db import execute_query

def print_teacher_subjects():
    query = "SELECT * FROM Teacher_Subject;"
    teacher_subjects = execute_query(query)
    print("\nПреподаватели и предметы:")
    for ts in teacher_subjects:
        print(ts)

def add_teacher_subject(teacher_id, subject_name):
    query = "INSERT INTO Teacher_Subject (teacher_id, subject_name) VALUES (%s, %s);"
    execute_query(query, (teacher_id, subject_name), fetch=False)
    print(f"Добавлен предмет '{subject_name}' для преподавателя ID: {teacher_id}")

def delete_teacher_subject(teacher_id, subject_name):
    query = "DELETE FROM Teacher_Subject WHERE teacher_id = %s AND subject_name = %s;"
    execute_query(query, (teacher_id, subject_name), fetch=False)
    print(f"Удален предмет '{subject_name}' для преподавателя ID: {teacher_id}")

def get_teacher_subjects(teacher_id):
    query = "SELECT * FROM Teacher_Subject WHERE teacher_id = %s;"
    subjects = execute_query(query, (teacher_id,))
    result = subjects
    print(result)  
    return result