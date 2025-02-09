from db import execute_query

def print_control_works():
    query = "SELECT * FROM Control_Work;"
    control_works = execute_query(query)
    print("\nКонтрольные работы:")
    for control in control_works:
        print(control)

def add_control_work(name, subject_name):
    query = "INSERT INTO Control_Work (name, subject_name) VALUES (%s, %s) RETURNING id;"
    result = execute_query(query, (name, subject_name))
    if result:
        print(f"Добавлена контрольная работа с ID: {result[0]['id']}")

def delete_control_work(control_work_id):
    query = "DELETE FROM Control_Work WHERE id = %s RETURNING id;"
    result = execute_query(query, (control_work_id,))
    if result:
        print(f"Удалена контрольная работа с ID: {result[0]['id']}")

def get_control_work(control_work_id):
    query = "SELECT * FROM Control_Work WHERE id = %s;"
    control_work = execute_query(query, (control_work_id,))
    result = control_work[0] if control_work else None
    print(result)  
    return result