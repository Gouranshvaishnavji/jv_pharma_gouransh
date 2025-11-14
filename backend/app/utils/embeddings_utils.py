from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

def get_embedding_model():
    if settings.GEMINI_API_KEY:
        return GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    else:
        from langchain.embeddings import FakeEmbeddings
        return FakeEmbeddings(size=768)

def embed_texts(texts):
    model = get_embedding_model()
    return model.embed_documents(texts)
