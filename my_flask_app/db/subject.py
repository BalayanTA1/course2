from db.db import execute_query

def print_subjects():
    query = "SELECT * FROM Subject;"
    subjects = execute_query(query)
    print("\nПредметы:")
    for subject in subjects:
        print(subject)

def add_subject(name):
    query = "INSERT INTO Subject (name) VALUES (%s);"
    execute_query(query, (name,), fetch=False)
    print(f"Добавлен предмет: {name}")

def delete_subject(name):
    query = "DELETE FROM Subject WHERE name = %s;"
    execute_query(query, (name,), fetch=False)
    print(f"Удален предмет: {name}")

def get_subject(name):
    query = "SELECT * FROM Subject WHERE name = %s;"
    subject = execute_query(query, (name,))
    result = subject[0] if subject else None
    print(result)  
    return result

def get_subject_name():
    query = "SELECT name FROM Subject;"
    subjects = execute_query(query)
    return [{'name': subject['name']} for subject in subjects]