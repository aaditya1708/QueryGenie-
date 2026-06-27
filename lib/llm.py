import google.generativeai as genai
import os
from dotenv import load_dotenv

def generate_sql_query(query,retrived_schema):
    context = "\n\n".join(
        retrived_schema["documents"][0]
    )
    prompt = f"""
    You are an expert SQLite SQL generator.
    Your task is to generate a valid SQLite SQL query based ONLY on the provided database schema.
    Rules:
    1. Use ONLY the tables and columns present in the schema.
    2. Generate ONLY SQLite-compatible SQL.
    3. Do NOT assume tables or columns that are not in the schema.
    4. Return ONLY the SQL query.
    5. Do NOT include explanations.
    6. Do NOT use markdown or ```sql``` code fences.
    7. If the question cannot be answered using the provided schema, return exactly:
   CANNOT_GENERATE_SQL
    Database Schema:
    {context}
    User Question:
    {query}
    SQL Query:
    """
    load_dotenv()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    response = model.generate_content(prompt)
    return response.text.strip()