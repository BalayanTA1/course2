from db import execute_query

def print_institutes():
    query = "SELECT * FROM Institute;"
    institutes = execute_query(query)
    print("\nИнституты:")
    for institute in institutes:
        print(institute)

def add_institute(name):
    query = "INSERT INTO Institute (name) VALUES (%s) RETURNING id;"
    result = execute_query(query, (name,), fetch=True)
    if result:
        print(f"Добавлен институт с ID: {result[0]['id']}")

def delete_institute(institute_id):
    query = "DELETE FROM Institute WHERE id = %s RETURNING id;"
    result = execute_query(query, (institute_id,), fetch=True)
    if result:
        print(f"Удален институт с ID: {result[0]['id']}")

def get_institute(institute_id):
    query = "SELECT * FROM Institute WHERE id = %s;"
    result = execute_query(query, (institute_id,), fetch=True)
    result = result[0] if result else None
    print(result) 
    return result