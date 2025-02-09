import psycopg2
from psycopg2.extras import RealDictCursor

db_config = {
    'host': 'localhost',
    'database': '123',
    'user': '123',
    'password': '123'
}

def get_db_connection():
    conn = psycopg2.connect(**db_config)
    return conn

# Функция для выполнения SQL-запроса и возврата результата
def execute_query(query, params=None, fetch=True):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute(query, params)
        if fetch:
            result = cur.fetchall()
        else:
            result = None
        conn.commit()  # Подтверждаем изменения
        return result
    except Exception as e:
        conn.rollback()  # Откатываем изменения в случае ошибки
        print(f"Ошибка при выполнении запроса: {e}")
        raise
    finally:
        cur.close()
        conn.close()