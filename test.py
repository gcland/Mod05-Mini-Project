from connect_mysql import connect_database
from mysql.connector import Error
conn = connect_database()
if conn is not None:
    try:
        cursor = conn.cursor()
        cursor = conn.cursor(buffered=True)
        auth_name = 'Grant'
        view_auth = (auth_name, )
        query = "Select * from authors\nWHERE name = %s"
        cursor.execute(query, view_auth)
        conn.commit()
        for row in cursor.fetchall():
            print(f"Author ID#: {row[0]}, Author Name: {row[1]}, Biography: {row[2]}.")

    except Error as e:
        print(f"Error: {e}")    