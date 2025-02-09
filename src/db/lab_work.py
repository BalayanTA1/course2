from db import execute_query

def print_lab_works():
    query = "SELECT * FROM Lab_Work;"
    lab_works = execute_query(query)
    print("\nЛабораторные работы:")
    for lab in lab_works:
        print(lab)

def add_lab_work(name, subject_name):
    query = "INSERT INTO Lab_Work (name, subject_name) VALUES (%s, %s) RETURNING id;"
    result = execute_query(query, (name, subject_name))
    if result:
        print(f"Добавлена лабораторная работа с ID: {result[0]['id']}")

def delete_lab_work(lab_work_id):
    query = "DELETE FROM Lab_Work WHERE id = %s RETURNING id;"
    result = execute_query(query, (lab_work_id,))
    if result:
        print(f"Удалена лабораторная работа с ID: {result[0]['id']}")

def get_lab_work(lab_work_id):
    query = "SELECT * FROM Lab_Work WHERE id = %s;"
    lab_work = execute_query(query, (lab_work_id,))
    result = lab_work[0] if lab_work else None
    print(result)  
    return result