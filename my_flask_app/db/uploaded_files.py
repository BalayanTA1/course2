from db.db import execute_query

def insert_uploaded_file(student_id, work_number, file_path):
    query = "INSERT INTO Uploaded_Files (student_id, work_number, file_path) VALUES (%s, %s, %s)"
    params = (student_id, work_number, file_path)
    execute_query(query, params, fetch=False)