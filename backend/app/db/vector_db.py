from langchain_community.vectorstores import Chroma
from app.utils.embeddings_utils import get_embedding_model
from app.core.config import settings

def init_db(persist_directory=None):
    if persist_directory is None:
        persist_directory = settings.VECTOR_DB_PATH
    embeddings = get_embedding_model()
    db = Chroma(
        collection_name="medical_docs",
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )
    return db

def add_documents(chunks):
    db = init_db()
    texts = [c["text"] for c in chunks]
    metadatas = [
        {
            "doc_id": c["doc_id"],
            "chunk_id": c["chunk_id"],
            "source_path": c["source_path"],
            "start_char": c["start_char"],
            "end_char": c["end_char"],
        }
        for c in chunks
    ]
    db.add_texts(texts, metadatas=metadatas)
    db.persist()
    return len(chunks)

def query_vector_db(query, k=5):
    db = init_db()
    docs = db.similarity_search(query, k=k)
    results = []
    for d in docs:
        meta = d.metadata
        results.append(
            {
                "text": d.page_content,
                "metadata": {
                    "doc_id": meta.get("doc_id"),
                    "chunk_id": meta.get("chunk_id"),
                    "source_path": meta.get("source_path"),
                    "char_range": f"{meta.get('start_char')}–{meta.get('end_char')}",
                },
            }
        )
    return results
