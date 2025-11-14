from app.db.vector_db import query_vector_db
from app.core.session_manager import add_message, get_session_history
from langchain_core.prompts import PromptTemplate
from app.utils.embeddings_utils import get_embedding_model

def get_answer(query, session_id=None, k=5):
    past = get_session_history(session_id) if session_id else []

    docs = query_vector_db(query, k)
    if not docs:
        answer = "Information not found in uploaded documents."
        if session_id:
            add_message(session_id, "user", query)
            add_message(session_id, "assistant", answer)
        return {"answer": answer, "citations": []}

    context = "\n\n".join(d["text"] for d in docs)
    citations = [d["metadata"] for d in docs]

    llm = get_embedding_model()   # placeholder until i use real LLM
    answer = context[:700]

    if session_id:
        add_message(session_id, "user", query)
        add_message(session_id, "assistant", answer)

    return {"answer": answer, "citations": citations}
