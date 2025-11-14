### Backend: FastAPI (Python)

FastAPI is used as the backend framework because it is lightweight, fast, and easy to structure. It also automatically generates API documentation at `/docs`, which speeds up testing.  
The backend exposes routes for file uploads, chat queries, health checks, and session handling. It also coordinates extraction, chunking, and retrieval.

---

### Python as the Core Language

Python was chosen because most AI tooling and document-processing libraries are built around it. Libraries for PDFs, embeddings, extraction, and vector databases are mature and easy to integrate. This makes Python a natural fit for a text-heavy pipeline like this one.

---

### Frontend: React + Vite

The frontend is a simple React application built using Vite. The interface handles document uploads and provides a chat UI for interacting with the assistant. Vite was chosen because it is fast, modern, and easier to work with during development compared to older tooling.

---

### Document Extraction Libraries

To extract text from various document types, the project uses:

- `pdfplumber` for PDFs  
- `python-docx` for Word files  
- direct text reading for `.txt` files  

These libraries allow the system to support common medical document formats without relying on paid services or heavy OCR tools.

---

### Text Cleaning and Chunking

After extraction, document text goes through a cleaning step and then is chunked into smaller segments. Chunking is necessary to prepare the text for embeddings. The system uses around 1000-character chunks with overlap to help preserve context.  
Chunk metadata is stored (file name, chunk number, start and end character positions), which is later used for citations.

---

### Local Embeddings (Sentence Transformers)

Instead of using Gemini embeddings—which are not free—the system uses the `sentence-transformers/all-MiniLM-L6-v2` model.  
It runs locally on CPU, costs nothing, and produces high-quality semantic embeddings suitable for retrieval tasks.  
This avoids quota issues and keeps the pipeline fully offline.

---

### Vector Database: ChromaDB (PersistentClient)

ChromaDB is used to store embeddings and perform similarity search. The PersistentClient version saves data to disk so that the vector store persists across restarts.  
Chroma is simple to work with, requires no external server, and is a reliable choice for retrieving relevant document chunks based on user queries.

---

### LLM Layer: Gemini 1.5 Flash

Gemini 1.5 Flash is used for generating the final answer. The pipeline retrieves chunks from Chroma, formats them with the question, and sends them to Gemini with instructions to answer strictly based on the provided context.  
This keeps answers grounded and reduces hallucination. The model is only used for answering, not for embeddings.

---

### Limited Use of LangChain

LangChain is used only for essential components like prompt templates and LLM invocation.  
The rest of the pipeline—chunking, embedding, vector storage—is implemented directly to avoid unnecessary complexity.  
This keeps the system more understandable and maintains control over the logic.

---

### Local File Storage

Uploaded files are stored inside:

data/uploads/<uuid>/

pgsql
Copy code

This folder structure ensures each upload is isolated. It also helps maintain proper links for citations because each chunk includes the path to the original file.

---

### Deployment and Containerization

The backend is set up so it can be containerized using Docker. This ensures consistent behavior across different machines since extraction libraries, embeddings, and Chroma all run inside the same container.  
The frontend can be deployed independently on platforms like Vercel, while the backend can be deployed on container-friendly platforms such as Render, Railway, or Fly.io.

---

### Summary

In summary, the stack is designed to be practical rather than over-engineered. FastAPI handles the API layer, Python provides access to all the necessary AI libraries, ChromaDB manages retrieval, Sentence Transformers supply free embeddings, and Gemini provides grounded final answers.  
The combination results in a complete medical document assistant that remains inexpensive and easy to