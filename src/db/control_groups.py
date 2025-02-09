from db import execute_query

def print_control_groups():
    query = "SELECT * FROM Control_Groups;"
    control_groups = execute_query(query)
    print("\nКонтрольные группы:")
    for cg in control_groups:
        print(cg)

def add_control_group(date, group_number, control_work_id, subject_name):
    query = "INSERT INTO Control_Groups (date, group_number, control_work_id, subject_name) VALUES (%s, %s, %s, %s);"
    execute_query(query, (date, group_number, control_work_id, subject_name), fetch=False)
    print(f"Добавлена контрольная группа для группы номер: {group_number}")

def delete_control_group(group_number, control_work_id):
    query = "DELETE FROM Control_Groups WHERE group_number = %s AND control_work_id = %s;"
    execute_query(query, (group_number, control_work_id), fetch=False)
    print(f"Удалена контрольная группа для группы номер: {group_number}")

def get_control_groups(group_number):
    query = "SELECT * FROM Control_Groups WHERE group_number = %s;"
    control_groups = execute_query(query, (group_number,))
    result = control_groups
    print(result)  
    return result