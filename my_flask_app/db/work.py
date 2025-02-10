from db.db import execute_query

def get_student_tasks(student_id):
    query = """
        SELECT 
            w.subject_name AS discipline,
            w.work_number AS number,
            w.name AS title,
            CASE 
                WHEN w.is_lab THEN 'Лабораторная'
                WHEN w.is_control THEN 'Контрольная'
            END AS type,
            wg.deadline AS deadline,
            wr.submission_date AS submission_date,
            wr.grade AS grade
        FROM Work w
        JOIN Work_Groups wg ON w.work_number = wg.work_number
        LEFT JOIN Work_Result wr ON w.work_number = wr.work_number AND wr.student_id = %s
        WHERE wg.group_number = (SELECT group_number FROM Student WHERE student_id = %s)
    """
    params = (student_id, student_id)
    tasks = execute_query(query, params)
    return tasks