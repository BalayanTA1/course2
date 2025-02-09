from db import execute_query

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