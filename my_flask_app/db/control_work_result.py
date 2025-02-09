from db.db import execute_query

def print_control_results():
    query = "SELECT * FROM Control_Work_Result;"
    results = execute_query(query)
    print("\nРезультаты контрольных работ:")
    for result in results:
        print(result)

def add_control_work_result(grade, student_id, control_work_id, subject_name):
    query = "INSERT INTO Control_Work_Result (grade, student_id, control_work_id, subject_name) VALUES (%s, %s, %s, %s);"
    execute_query(query, (grade, student_id, control_work_id, subject_name), fetch=False)
    print(f"Добавлен результат контрольной работы для студента ID: {student_id}")

def delete_control_work_result(student_id, control_work_id):
    query = "DELETE FROM Control_Work_Result WHERE student_id = %s AND control_work_id = %s;"
    execute_query(query, (student_id, control_work_id), fetch=False)
    print(f"Удален результат контрольной работы для студента ID: {student_id}")

def get_control_work_result(student_id, control_work_id):
    query = "SELECT * FROM Control_Work_Result WHERE student_id = %s AND control_work_id = %s;"
    result = execute_query(query, (student_id, control_work_id))
    result = result[0] if result else None
    print(result)  
    return result