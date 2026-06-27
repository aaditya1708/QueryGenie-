from sentence_transformers import SentenceTransformer

embeder = SentenceTransformer("all-MiniLM-L6-v2")
def embed_query(query):
    query_embeddings = embeder.encode(query)
    return query_embeddings

def retrive_schema(query_embedding,collection):
    result = collection.query(
        query_embeddings = [query_embedding.tolist()],
        n_results = 3
    )
    return result

def retrival_pipeline(query,collection):
    query_embedding = embed_query(query)
    retrived_schema = retrive_schema(query_embedding,collection)
    return retrived_schema