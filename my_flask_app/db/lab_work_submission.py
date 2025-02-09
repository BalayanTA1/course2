from db import execute_query

def print_lab_submissions():
    query = "SELECT * FROM Lab_Work_Submission;"
    submissions = execute_query(query)
    print("\nСдача лабораторных работ:")
    for submission in submissions:
        print(submission)

def add_lab_work_submission(submission_date, student_id, lab_work_id, subject_name):
    query = "INSERT INTO Lab_Work_Submission (submission_date, student_id, lab_work_id, subject_name) VALUES (%s, %s, %s, %s);"
    execute_query(query, (submission_date, student_id, lab_work_id, subject_name), fetch=False)
    print(f"Добавлена сдача лабораторной работы для студента ID: {student_id}")

def delete_lab_work_submission(student_id, lab_work_id):
    query = "DELETE FROM Lab_Work_Submission WHERE student_id = %s AND lab_work_id = %s;"
    execute_query(query, (student_id, lab_work_id), fetch=False)
    print(f"Удалена сдача лабораторной работы для студента ID: {student_id}")

def get_lab_work_submission(student_id, lab_work_id):
    query = "SELECT * FROM Lab_Work_Submission WHERE student_id = %s AND lab_work_id = %s;"
    submission = execute_query(query, (student_id, lab_work_id))
    result = submission[0] if submission else None
    print(result)  
    return result