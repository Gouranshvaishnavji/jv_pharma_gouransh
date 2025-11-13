**finalised folder structure**
backend/
│
├── app/
│   ├── main.py                     # Entry point (FastAPI app)
│   ├── core/
│   │   ├── config.py               # Env vars, settings (dotenv / pydantic)
│   │   └── logger.py               # Logging setup
│   │
│   ├── db/
│   │   ├── vector_db.py            # Vector store init & retrieval
│   │
│   ├── models/
│   │   └── schemas.py              # Pydantic models for request/response
│   │
│   ├── services/
│   │   ├── document_service.py     # Extract + chunk + embed docs
│   │   ├── qa_service.py           # Handles LangChain pipeline
│   │   └── report_service.py       # For later phases (PDF report)
│   │
│   ├── controllers/ (or routers/)
│   │   ├── document_routes.py      # /upload endpoints
│   │   ├── chat_routes.py          # /chat endpoints
│   │   └── report_routes.py        # /report (later)
│   │
│   ├── utils/
│   │   ├── file_utils.py           # Save files, detect type
│   │   ├── text_utils.py           # Clean, chunk, summarize
│   │   └── embeddings_utils.py     # Embedding functions
│   │
│   └── tests/
│       ├── test_upload.py
│       ├── test_chat.py
│       └── conftest.py
│
├── requirements.txt
├── .env
└── Dockerfile  (later)

Phase 1 — MVP (no Drive, local upload-only, full-stack)

Goal: runnable React + FastAPI app where users upload docs, docs are parsed + indexed, chat uses only uploaded docs, and answers include chunk citations.

1. Project bootstrap

Create repository and branches (main, dev, mvp) * done *

Acceptance: git repo initialized, branches created *done*

 Create project skeleton (folders) *done*

backend/app/... (use structure we previously discussed) *done*

frontend/ (React app created with Vite or create-react-app) **done******

infra/ (for Dockerfiles, docker-compose) *done*

Acceptance: folders present, README placeholder *done*

2. Backend basics

 Create main.py + app creation *done*

Add FastAPI() instance, root health route /

Acceptance: uvicorn app.main:app --reload returns 200 on /

Quick test: curl http://localhost:8000/

 Add CORS middleware configured for frontend origin

Acceptance: browser can call API from http://localhost:3000 without CORS errors

 Add structured logger app/core/logger.py

Acceptance: logs printed for requests

3. API routes & modular routers

 Implement controllers/document_routes.py:

POST /api/docs/upload accepting multiple files (UploadFile)

returns upload metadata (file name, size, saved path)

Acceptance: upload works via curl -F "files=@file.pdf" http://localhost:8000/api/docs/upload

 Implement controllers/chat_routes.py:

POST /api/chat/ask with body { "query": "...", "session_id": optional }

Acceptance: endpoint returns valid JSON for empty DB (see next)

 Add API docs accessible at /docs

Acceptance: OpenAPI UI shows routes

4. File handling (save + canonicalize)

 Implement utils/file_utils.py:

Save uploaded files to data/uploads/<uuid>/<original_name>

Return metadata (path, mimetype)

Acceptance: files saved correctly, permissions OK

 Add file-type detection (mime) and size limits (env-configurable)

Acceptance: reject > limit or unsupported mime with 400

5. Plaintext extraction pipeline

 Add extractors:

extract_text_pdf(file_path): PyPDF2 or pdfplumber fallback

extract_text_docx(file_path): python-docx

extract_text_txt(file_path): plain read

extract_text_image(file_path): pytesseract (optional MVP; at least placeholder)

Acceptance: extracted plain text stored as .txt alongside original

 Unit tests for each extractor with small example files

6. Text cleaning + chunking

 Implement text_utils.py:

Normalize whitespace, remove control chars, keep original order

Chunking using LangChain’s RecursiveCharacterTextSplitter or custom: chunk_size=1000, overlap=100

Produce metadata per chunk: {doc_id, chunk_id, start_char, end_char, source_path}

Acceptance: chunks stored as JSON lines per document

7. Embeddings + vector store

 Pick local dev vector DB (Chroma recommended) and implement wrapper db/vector_db.py

Functions: init_db(), add_documents(chunks), query(query, k=5), persist(), load()

Acceptance: can add_documents then query returns candidate chunks

 Implement embeddings adapter utils/embeddings_utils.py:

Start with OpenAI or local dummy embedding (if API key not set) so MVP tests run offline

Provide interface for later swap to Gemini embeddings

Acceptance: generates numeric vectors and index inserts succeed

 Persist vector DB to disk and load on startup

Acceptance: restart service, index still available

8. Retrieval + QA chain (LangChain)

 Implement services/qa_service.py:

Given query, call retriever to get k chunks

Build a prompt template that instructs LLM to answer ONLY from provided chunks and to explicitly say "NOT_FOUND" if absent

Include chunk citations in the LLM prompt and instruct to return a structured JSON:

{ answer: "...", citations: [ { doc_path, chunk_id, text_snippet } ] }

Acceptance: For queries matching docs, answer is grounded and contains citations

 Safety: if retriever returns low relevance or empty, return {"answer": "Information not found in uploaded documents."}

Acceptance: endpoint does not hallucinate for unrelated queries

9. Citation mechanics

 When indexing, store per-chunk metadata including:

doc_id, doc_name, local_path, chunk_id, char_range

 Ensure QA response references doc_name + chunk_id + char_range and snippet

Acceptance: Chat response contains clickable local path (or full path) so user can open file

10. Conversation / Session memory (short-lived)

 Implement session management:

session_id parameter in chat; store conversation context in Redis (or in-memory for MVP)

Store last N (configurable) turns with metadata

Acceptance: follow-up question that refers to previous answer is handled using stored context

 Add endpoint POST /api/chat/new_session and POST /api/chat/end_session

Acceptance: sessions start/close successfully

11. Frontend minimal (React)

 Scaffold React app with:

File upload UI (multi-file)

Chat UI (message list, input box)

Display citations and allow opening local links (download)

Acceptance: can upload, see upload success, and send a query to backend

 Connect to /api/docs/upload and /api/chat/ask using fetch/axios

 Handle CORS & errors gracefully

12. Tests & CI

 Write pytest unit tests for:

Extractors

Chunker

Vector DB wrapper (add/query)

Chat endpoint behavior for known fixtures

 Add github/workflows/ci.yml for running tests on PR

Acceptance: tests run and pass in CI

13. Logging / Observability

 Add LangSmith or basic request tracing stub (if API keys not present, logs should show placeholders)

 Log retrieval ranking scores and chosen chunks for debug

14. Acceptance checklist for MVP

 Upload a set of docs

 Ask a question that is answered correctly and cites the exact chunk & document

 Ask a question NOT in docs → receive explicit "Information not found..."

 Follow-up question referencing prior answer works (session-based)

 Frontend can trigger upload, ask, and display results

 Phase 2 — Citation / Reference improvements & Drive prep

Goal: improve citation format and prepare for Google Drive integration (links etc.)

1. Citation format standard

 Define canonical citation object:

{
  "doc_id": "uuid",
  "doc_name": "report.pdf",
  "source": "upload|drive",
  "path_or_link": "/data/uploads/.. or https://drive.google.com/..",
  "chunk_id": "c_0001",
  "char_range": [0, 456],
  "snippet": "first 200 chars..."
}


Acceptance: QA responses include this object

2. Add rich response from backend

 Return structured response: { answer, citations: [...], provenance: {...} }

 Make frontend render citations as clickable links (drive links open new tab)

Acceptance: clicking link opens file (local download or drive page)

3. Prepare for Drive metadata model

 Add source_type field in DB schema (upload vs drive)

 Ensure chunk metadata supports drive_file_id and drive_link

Acceptance: indexes can hold drive metadata without Drive being integrated yet

 Phase 3 — Google Drive Integration & Drive-based citations

Goal: read files from a provided Google Drive (user grants access), index them, and include Drive links in citations.

Note: Drive integration requires OAuth and careful permission/scopes. I’m including explicit tasks for security and QA.

1. Google OAuth setup

 Create Google Cloud project & enable Drive API (document steps in README)

 Configure OAuth consent screen, create credentials (client_id, client_secret)

 Store secrets in env / secret manager

Acceptance: credential file present and secrets are environment-configured

2. Backend endpoints for Drive auth

 GET /api/drive/auth_url → returns OAuth URL

 GET /api/drive/oauth_callback?code=... → exchange code for refresh token, store user tokens securely

 Protect callback route with state parameter to mitigate CSRF

Acceptance: Auth flow completes and tokens stored per user session

3. Drive file listing + selective import

 GET /api/drive/files → list files (name, id, mimetype, modifiedTime)

 POST /api/drive/import with list of file_ids → download file content, save to data/drive/<user_id>/..., run extraction + chunk + index

Acceptance: selected drive files appear in index with source=drive

4. Drive citation linking

 When creating chunk metadata for drive files, set path_or_link to https://drive.google.com/file/d/<fileId>/view

 Ensure QA responses include these drive links and they open with proper access

Acceptance: clicking citation drive link opens Drive file (if user has permission)

5. Refresh tokens & token rotation

 Implement token refresh logic and secure storage (encrypted)

Acceptance: long-running sessions can keep using Drive without re-authenticate

6. Privacy & security checks

 Prompt users to grant only necessary scopes (read-only)

 Provide UI to deauthorize Drive access and delete indexed Drive files

Acceptance: user can revoke and confirm removal from index

 Phase 4 — Report generation (structured medical reports)

Goal: let user request a report composed of exact extracted content (tables/figures preserved), plus optional summaries; export as downloadable PDF.

1. Document element extraction (tables/figures)

 Use pdfplumber or camelot/tabula for tables; pdf2image + OCR for images if needed

 Implement services/report_service.py functions:

extract_tables(file_path) -> list[table objects]

extract_images(file_path) -> list[image objects]

extract_exact_text(doc, section_locator) -> exact text

Acceptance: extracted tables are serializable (CSV/JSON) and images are saved as PNGs

2. LLM function calling orchestration

 Create LLM function signatures (LangChain function-calling or LLM-native)

e.g., get_relevant_sections(query, sections) returns list of chunk references

 Implement safe function that maps user-selected sections → extraction calls

Acceptance: calling the function returns structured extraction plan

3. Report composition

 Report template system (Jinja2 or HTML template)

Sections: Introduction, Clinical Findings, Patient Tables, Graphs, Summary

Preserve extracted tables/images in their original format within report

 If user requests a summary for a section, call LLM to produce concise summary and append

Acceptance: final report HTML renders with exact data and summaries where requested

4. PDF generation

 Use WeasyPrint or wkhtmltopdf to convert HTML → PDF

 Endpoint POST /api/report/generate that returns application/pdf or URL to download

Acceptance: PDF downloads and images/tables look correct; exact text matches source (verifiable via checksum)

5. Provenance & citations inside report

 Each inserted element (table/image/text) must include citation metadata (doc name, page, chunk_id)

Acceptance: report contains properly formatted references per element

 Phase 5 — Dockerization + Nginx (optional but recommended)

Goal: containerize backend & frontend, create compose file for local deployment, provide Nginx reverse proxy for production-like behavior.

1. Dockerfiles

 backend/Dockerfile:

Use slim Python base, install deps, copy code, expose port 8000, set uvicorn start command

 frontend/Dockerfile:

Build React app and serve with nginx or serve

Acceptance: docker build for both succeeds locally

2. docker-compose.yml

 Compose file with services:

backend (FastAPI)

frontend (React)

vector_db (if using a containerized Chroma DB or Redis)

redis (for session store)

Acceptance: docker-compose up brings up the stack; services can talk via internal network

3. Nginx reverse proxy (production config)

 Create infra/nginx/nginx.conf:

Proxy /api to backend, serve static frontend files

Add TLS termination placeholders (for production, use certs)

 Add health checks and basic rate-limit rules (limit reqs per IP)

Acceptance: reverse proxy routes traffic correctly

4. Docker security & image size

 Multi-stage builds to reduce size

 Set non-root user, proper environment variables, .dockerignore

Acceptance: images are minimized and non-root runtime user used

 Phase 6 — Deployment, Monitoring & Scalability

Goal: production-ready deployment outline, autoscaling, basic monitoring, logging, alerting.

1. Deployment target (choose one)

 Cloud VM (e.g., GCP VM / AWS EC2) + docker-compose — simplest

 Container service (GCP Cloud Run / AWS ECS / Azure Container Instances)

 Kubernetes cluster (EKS/GKE/AKS) — for scale

Acceptance: chosen option documented and manifests provided

2. CI/CD pipeline

 GitHub Actions:

ci for tests

build & push Docker images to registry

deploy to staging cluster

Acceptance: pipeline triggers on PR merges

3. Monitoring + Logging

 Centralized logs: integrate with ELK/Cloud logging or a hosted service (Logflare/Datadog)

 Metrics: Prometheus + Grafana or cloud metrics

 Instrument endpoints with request latency, errors, retrieval counts

Acceptance: dashboards show uptime and API latencies

4. Alerts

 Alert on:

Errors > threshold

Vector DB size warnings

High response latencies

Acceptance: test alert triggers in staging

5. Autoscaling & performance

 Prepare for horizontal scaling:

Stateless backend (store sessions in Redis)

Vector DB must be shared/persisted (hosted Chroma or vector DB service)

 Load test with locust or k6 to identify bottlenecks

 Add rate limiting and request throttling

Acceptance: able to sustain target RPS (documented in README)

6. Backup & Data retention

 Backup vector DB periodically

 Provide data deletion endpoints for compliance (GDPR/HIPAA-like)

Acceptance: backups can be restored in staging

 Phase 7 — README, demo video, architecture diagram, and final deliverables

Goal: produce neat docs and assets required for the hiring task.

1. README content checklist

 Project overview & goals

 Tech stack (frontend, backend, vector DB, LLM adapter)

 Local dev quickstart (env vars, how to run frontend+backend)

 How to run tests & linting

 How to build Docker images & docker-compose

 Google Drive setup (steps to create credentials)

 Deployment instructions (one or two supported methods)

 Architecture diagram (link to image)

 API reference (endpoints and example requests)

 Security & privacy notes (token storage, scopes, data removal)

Acceptance: README provides enough to run a local MVP

2. Demo video (2–3 minutes)

 Script:

20s: one-line overview and tech stack

30s: demo upload + indexing

40s: ask a question, show citation and open file

20s: generate a small structured report and download PDF

10s: mention deployment & future work

 Record screen, voiceover, and host in repo (or link)

Acceptance: video demonstrates all MVP flows clearly

3. Architecture diagram

 Diagram elements:

Frontend, Nginx, FastAPI, Vector DB, LLM (external), Google Drive oauth, Redis, Monitoring

Dataflow arrows for Upload → Extract → Chunk → Embed → Index → Query → LLM

 Include notes on scaling, persistence, and security boundaries

Acceptance: diagram PNG/SVG added to repo

4. Final repo checklist

 Code documented & commented

 CONTRIBUTING.md and LICENSE

 All env var defaults and example .env.example

 Tests and CI pipeline present

Acceptance: everything needed for reviewer to run MVP locally

 Extra developer-level checks (quality & scalability)

 Use typed Python (mypy) and linting (ruff/flake8)

 Add resource limits and graceful shutdown handlers (SIGTERM)

 Ensure large file uploads stream to disk, avoid memory blowup

 Limit concurrency (uvicorn workers) config documented

 Secrets never committed (use .env + secret manager)

 Add integration tests that run the whole upload → query flow with fixtures