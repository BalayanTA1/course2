from db.db import execute_query

def check_existing_grade(student_id, work_number):
    query = """
        SELECT * FROM Work_Result
        WHERE student_id = %s AND work_number = %s
    """
    return execute_query(query, (student_id, work_number))

def update_grade(student_id, work_number, grade, submission_date):
    update_query = """
        UPDATE Work_Result
        SET grade = %s, submission_date = %s
        WHERE student_id = %s AND work_number = %s
    """
    execute_query(update_query, (grade, submission_date, student_id, work_number), fetch=False)

def insert_grade(student_id, work_number, grade, submission_date):
    insert_query = """
        INSERT INTO Work_Result (grade, submission_date, student_id, work_number, subject_name)
        VALUES (%s, %s, %s, %s, (SELECT subject_name FROM Work WHERE work_number = %s))
    """
    execute_query(insert_query, (grade, submission_date, student_id, work_number, work_number), fetch=False)