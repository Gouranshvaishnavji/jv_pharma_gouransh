from app.db.vector_db import query_vector_db
from langchain_core.prompts import PromptTemplate
from app.utils.embeddings_utils import get_embedding_model

def get_answer(query, k=5):
    docs = query_vector_db(query, k)
    if not docs:
        return {"answer": "Information not found in uploaded documents.", "citations": []}

    context = "\n\n".join([d["text"] for d in docs])
    citations = [d["metadata"] for d in docs]

    prompt = PromptTemplate.from_template("""
    You are a medical assistant.
    Use only the provided context to answer.
    If not found, respond exactly: "Information not found in uploaded documents."

    Context:
    {context}

    Question:
    {question}

    Answer only with relevant facts from the context.
    """)

    llm = get_embedding_model()  # placeholder until Gemini LLM is integrated
    answer = context[:800]  # simulate grounded summary for now

    return {"answer": answer, "citations": citations}
