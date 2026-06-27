# QueryGenie

QueryGenie is a Text-to-SQL Retrieval-Augmented Generation (RAG) application that enables users to interact with SQLite databases using natural language. Users can upload a SQLite database, ask questions in plain English, and the system generates executable SQLite queries based on the database schema.

Unlike traditional Text-to-SQL systems that provide the entire schema to the language model, QueryGenie retrieves only the relevant schema using semantic search before generating SQL. This reduces unnecessary context and improves query generation.

---

## Features

- Upload any SQLite database
- Automatic database schema extraction
- Semantic schema retrieval using ChromaDB
- Natural language to SQLite SQL generation
- SQL validation before execution
- Support for:
  - SELECT
  - INSERT
  - UPDATE
  - DELETE
  - CREATE
  - ALTER
- Execute generated SQL
- Display query results in tabular format
- Download the updated database after modification queries

---

## Architecture

```
SQLite Database
      │
      ▼
Schema Extraction
      │
      ▼
LangChain Documents
      │
      ▼
Recursive Character Text Splitter
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
ChromaDB
      │
      ▼
Retriever
      │
      ▼
Relevant Schema
      │
      ▼
LLM
      │
      ▼
SQLite SQL
      │
      ▼
SQL Validation
      │
      ▼
SQLite Execution
      │
      ▼
Query Results
```

---

## Tech Stack

- Python
- Streamlit
- SQLite
- LangChain
- ChromaDB
- Sentence Transformers
- Gemini API 
- Pandas

---

## Project Structure

```
QueryGenie
│
├── app.py
├── requirements.txt
├── README.md
├── .env
│
├── chroma_db/
│
└── lib/
    ├── ingestion_pipeline.py
    ├── retrieval_pipeline.py
    ├── llm.py
    ├── sql_validator.py
    ├── sql_executor.py
    └── backend.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/<your-username>/QueryGenie.git
```

Navigate to the project directory

```bash
cd QueryGenie
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

For Gemini

```text
GOOGLE_API_KEY=YOUR_API_KEY
```
Run the application

```bash
streamlit run app.py
```

---

## Example Queries

### Read Operations

- Show all customers from Germany.
- List all albums created by AC/DC.
- Count the total number of customers.
- Show all playlists.
- Show all invoices where total is greater than 10.

### Modification Operations

- Insert a new artist named OpenAI Band.
- Update the city of customer with CustomerId 1 to Pune.
- Delete the artist named OpenAI Band.
- Create a table named Student with columns StudentId, Name and Age.

---

## Supported SQL Operations

- SELECT
- INSERT
- UPDATE
- DELETE
- CREATE
- ALTER

---

## Future Improvements

- PostgreSQL support
- MySQL support
- Query history
- Authentication
- Docker support
- Cloud deployment

---

## Author

**Aaditya Hole**

B.Tech Computer Engineering
