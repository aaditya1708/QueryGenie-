from lib.retrieval_pipeline import retrival_pipeline
from lib.llm import generate_sql_query
from lib.sql_validator import validate_sql_query
from lib.sql_executor import execute_sql_query

def backend_pipeline(query,collection,conn):
    retrived_schema = retrival_pipeline(query,collection)
    sql_query = generate_sql_query(query,retrived_schema)
    validation = validate_sql_query(sql_query)
    result = execute_sql_query(sql_query,validation,conn)
    return {
    "sql_query": sql_query,
    "result": result
    }
