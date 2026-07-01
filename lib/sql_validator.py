allowed_operation = {
    "SELECT",
    "UPDATE",
    "INSERT",
    "DELETE",
    "CREATE",
    "ALTER"
}


def validate_sql_query(sql_query):

    if not sql_query or not sql_query.strip():
        return {
            "is_valid": False,
            "operation": ""
        }

    sql_query = sql_query.strip()

    operation = sql_query.split()[0].upper()

    if operation in allowed_operation:
        return {
            "is_valid": True,
            "operation": operation
        }

    return {
        "is_valid": False,
        "operation": operation
    }