import sqlite3
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import uuid

def load_schema(cursor):
    documents = []

    # Get all table names
    cursor.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table';
    """)
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        # Get schema for current table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()

        # Create readable schema text
        schema_text = f"Table: {table_name}\n\nColumns:\n"

        for column in columns:
            schema_text += f"{column[1]} ({column[2]})\n"

        # Convert to LangChain Document
        document = Document(
            page_content=schema_text,
            metadata={
                "table_name": table_name
            }
        )

        documents.append(document)

    return documents

def split_documents(documents):
    spliter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 200
    )
    chunks = spliter.split_documents(documents)
    return chunks

embeder = SentenceTransformer("all-MiniLM-L6-v2")
def embed_chunks(chunks):
    chunks_text = [chunk.page_content for chunk in chunks]
    embeddings = embeder.encode(chunks_text)
    return embeddings

def store_embeddings(embeddings, chunks):
    client = chromadb.PersistentClient(path="./chroma_db")
    try:
        client.delete_collection("schema_collection")
    except:
        pass
    collection = client.get_or_create_collection(
        name="schema_collection"
    )
    collection.add(
        ids=[str(uuid.uuid4()) for _ in range(len(embeddings))],
        embeddings=embeddings.tolist(),
        documents=[chunk.page_content for chunk in chunks],
        metadatas=[chunk.metadata for chunk in chunks]
    )
    return collection

def ingestion_pipeline(cursor):
    documents = load_schema(cursor)
    chunks = split_documents(documents)
    embeddings = embed_chunks(chunks)
    collection = store_embeddings(embeddings,chunks)
    return collection