from db.db import execute_query

def get_works():
    query = "SELECT w.work_number, w.name, wg.subject_name, wg.group_number, wg.date, wg.deadline FROM Work w JOIN Work_Groups wg ON w.work_number = wg.work_number;"
    result = execute_query(query)
    return result

def delete_work_from_group(work_number, group_number):
    query = "DELETE FROM Work_Groups WHERE work_number = %s AND group_number = %s RETURNING work_number, group_number;"
    result = execute_query(query, (work_number, group_number))
    if result:
        print(f"Удалена работа с номером {result[0]['work_number']} из группы {result[0]['group_number']}")