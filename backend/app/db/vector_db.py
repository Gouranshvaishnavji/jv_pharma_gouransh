from chromadb import PersistentClient
from app.utils.embeddings_utils import get_embedding_model

DB_PATH = "data/vector_db"

def init_db():
    client = PersistentClient(path=DB_PATH)
    embeddings = get_embedding_model()

    collection = client.get_or_create_collection(
        name="medical_docs",
        metadata={"hnsw:space": "cosine"}
    )

    return collection, embeddings, client

def add_documents(chunks):
    collection, embeddings, client = init_db()

    texts = [chunk["text"] for chunk in chunks]
    metadatas = chunks
    ids = [f"chunk-{i}" for i in range(len(chunks))]

    vectors = embeddings.embed_documents(texts)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=vectors,
        metadatas=metadatas
    )

    return {"status": "indexed", "chunks": len(chunks)}

def query_vector_db(query, k=5):
    collection, embeddings, client = init_db()

    q_embedding = embeddings.embed_query(query)

    results = collection.query(
        query_embeddings=[q_embedding],
        n_results=k
    )

    return results
