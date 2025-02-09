from db.db import execute_query

def print_lab_groups():
    query = "SELECT * FROM Lab_Groups;"
    lab_groups = execute_query(query)
    print("\nЛабораторные группы:")
    for lg in lab_groups:
        print(lg)

def add_lab_group(deadline, group_number, lab_work_id, subject_name):
    query = "INSERT INTO Lab_Groups (deadline, group_number, lab_work_id, subject_name) VALUES (%s, %s, %s, %s);"
    execute_query(query, (deadline, group_number, lab_work_id, subject_name), fetch=False)
    print(f"Добавлена лабораторная группа для группы номер: {group_number}")

def delete_lab_group(group_number, lab_work_id):
    query = "DELETE FROM Lab_Groups WHERE group_number = %s AND lab_work_id = %s;"
    execute_query(query, (group_number, lab_work_id), fetch=False)
    print(f"Удалена лабораторная группа для группы номер: {group_number}")

def get_lab_groups(group_number):
    query = "SELECT * FROM Lab_Groups WHERE group_number = %s;"
    lab_groups = execute_query(query, (group_number,))
    result = lab_groups
    print(result)  
    return result