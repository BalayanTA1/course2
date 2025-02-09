from db.db import execute_query

def print_study_groups():
    query = "SELECT * FROM Study_Group;"
    groups = execute_query(query)
    print("\nГруппы:")
    for group in groups:
        print(group)

def add_study_group(institute_id):
    query = "INSERT INTO Study_Group (institute_id) VALUES (%s) RETURNING group_number;"
    result = execute_query(query, (institute_id,))
    if result:
        print(f"Добавлена группа с номером: {result[0]['group_number']}")

def delete_study_group(group_number):
    query = "DELETE FROM Study_Group WHERE group_number = %s RETURNING group_number;"
    result = execute_query(query, (group_number,))
    if result:
        print(f"Удалена группа с номером: {result[0]['group_number']}")

def get_study_group(group_number):
    query = "SELECT * FROM Study_Group WHERE group_number = %s;"
    group = execute_query(query, (group_number,))
    result = group[0] if group else None
    print(result)  
    return result

def get_study_group_numbers():
    query = "SELECT group_number FROM Study_Group;"
    group_numbers = execute_query(query)
    # Преобразуем данные в список словарей с ключом 'name'
    groups = [{'name': group['group_number']} for group in group_numbers]
    return groups