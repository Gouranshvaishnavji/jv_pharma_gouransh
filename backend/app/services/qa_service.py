from app.db.vector_db import query_vector_db
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from app.core.config import settings

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0.1
)


def get_answer(query, session_id=None):
    results = query_vector_db(query, k=5)

    if not results or not results["documents"] or len(results["documents"][0]) == 0:
        return {"answer": "Information not found in uploaded documents.", "citations": []}

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""
    citations = []

    for i, doc in enumerate(docs):
        m = metas[i]
        context += f"[Chunk {i} - {m['source_path']}]\n{doc}\n\n"
        citations.append({
            "chunk_id": i,
            "source": m["source_path"],
            "snippet": doc[:180]
        })

    prompt = f"""
You are a medical assistant. Answer using ONLY the provided context.
If answer is not present, reply: "Information not found in uploaded documents."

Context:
{context}

Question: {query}
Answer:
"""

    response = llm.invoke(prompt).content

    return {"answer": response, "citations": citations}
