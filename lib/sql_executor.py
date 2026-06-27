import pandas as pd

def execute_sql_query(sql_query, validation, conn):

    if not validation["is_valid"]:
        return {
            "status": "Error",
            "message": "Invalid SQL Query"
        }

    try:

        if validation["operation"] == "SELECT":

            df = pd.read_sql_query(sql_query, conn)

            return {
                "status": "Success",
                "operation": validation["operation"],
                "data": df
            }

        else:

            cursor = conn.cursor()
            cursor.execute(sql_query)
            conn.commit()

            return {
                "status": "Success",
                "operation": validation["operation"],
                "rows affected": cursor.rowcount
            }

    except Exception as e:

        conn.rollback()

        return {
            "status": "Error",
            "message": str(e)
        }