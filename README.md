# 📘 AI Research Mentor

**Upload a research paper. Understand it in plain English — for free, with a fully local LLM.**

AI Research Mentor is a Retrieval-Augmented Generation (RAG) application that lets anyone upload a research paper (PDF) and interactively explore it in beginner-friendly language — key concepts, methodology, architecture flow, datasets, conclusions, challenges, and more — without relying on any paid API. Inference runs entirely on a locally hosted open-weight LLM (Llama 3.2 1B via Ollama), so there are no API keys, no per-token costs, and no external dependency on OpenAI/Anthropic-style services.

---

## 🖼️ Architecture

<img width="1536" height="1024" alt="AI_Research Diagram" src="https://github.com/user-attachments/assets/e67d1b95-34da-4a40-8478-a440139309d2" />


The application is split into two independently deployed services:

- **Frontend** — a Streamlit app that handles PDF upload and the question/answer UI.
- **Backend** — a FastAPI service that owns the full RAG pipeline: PDF parsing, section-aware chunking, embedding generation, vector storage, retrieval, and local LLM generation.

They communicate over a simple REST API (`/upload-paper/`, `/ask/`).

---

## ✨ Features

- 📂 **PDF Upload & Parsing** — extracts and cleans text from research paper PDFs.
- 🧩 **Section-Aware Chunking** — text is parsed by logical paper sections (Abstract, Introduction, Methodology, Results, Conclusion, etc.) before chunking, so retrieval stays grounded in the right part of the paper.
- 🔎 **Semantic Retrieval** — chunks are embedded with `sentence-transformers` and stored in a ChromaDB vector store for similarity search.
- 🧠 **Local LLM Generation** — answers are generated entirely by a locally hosted Llama 3.2 1B model via Ollama. No API keys, no external inference cost.
- 🗂️ **One-Click Question Templates** — Beginner Explanation, Architecture Flow, Methodology, Key Concepts, Dataset Used, Conclusion, Challenges, Applications, and Research Gaps.
- ✍️ **Custom Question Support** — ask anything specific about the uploaded paper in natural language.
- 📊 **Auto-Generated Architecture Diagrams** — for architecture/workflow questions, the model synthesizes a Mermaid.js diagram rendered directly in the UI.
- 📚 **Verified Source Citations** — every answer is returned alongside the exact document section and chunk it was grounded in, so users can trace claims back to the paper.
- 🧵 **Conversational Memory** — retains recent conversation context across questions.
- 💸 **100% Free to Run** — designed to run entirely on free-tier infrastructure (Hugging Face Spaces + Streamlit Community Cloud), with no paid LLM API required.

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend API | FastAPI + Uvicorn |
| Local LLM Inference | Ollama (Llama 3.2 1B) |
| Embeddings | `sentence-transformers` (`all-MiniLM-L6-v2`) |
| Vector Store | ChromaDB |
| PDF Parsing | PyMuPDF |
| Containerization | Docker |
| Backend Hosting | Hugging Face Spaces (free CPU tier) |
| Frontend Hosting | Streamlit Community Cloud |

---

## 📁 Project Structure

```
.
├── app.py                   # FastAPI backend entrypoint (API routes)
├── streamlit_app.py         # Streamlit frontend (UI)
├── rag_pipeline.py          # Prompt construction + LLM generation logic
├── vector_store.py          # ChromaDB storage & similarity search
├── embedding_generator.py   # Sentence-transformer embedding model
├── section_parser.py        # Section-aware text parsing (regex-based)
├── text_chunker.py          # Chunking logic for indexing
├── text_cleaner.py          # Text normalization/cleanup
├── pdf_reader.py            # PDF text extraction (PyMuPDF)
├── reranker.py               # (Optional) chunk reranking
├── memory.py                 # Conversation memory helper
├── prompts.py                 # Prompt templates
├── ai_explainer.py           # Beginner-friendly explanation helpers
├── Dockerfile                # Backend container definition
├── entrypoint.sh              # Container startup script (Ollama + Uvicorn)
├── requirements.txt           # Backend Python dependencies
└── README.md
```

---

## ⚙️ How It Works (End-to-End Flow)

1. **Upload** — User uploads a PDF via the Streamlit frontend, which is sent to the FastAPI backend's `/upload-paper/` endpoint.
2. **Extract & Clean** — `pdf_reader.py` extracts raw text; `text_cleaner.py` normalizes it.
3. **Section Parsing** — `section_parser.py` detects section headers (Abstract, Introduction, Methodology, Results, Conclusion, etc.) using pattern matching and splits the paper accordingly.
4. **Chunking** — Each section is chunked independently via `text_chunker.py`, preserving section context per chunk.
5. **Embedding & Storage** — Chunks are embedded using `sentence-transformers` and stored in ChromaDB along with their section metadata.
6. **Question Asked** — User clicks a preset button or types a custom question, sent to `/ask/`.
7. **Retrieval** — The question is embedded with the *same* embedding model used for documents, and the top-matching chunks are retrieved from ChromaDB.
8. **Generation** — Retrieved chunks + the question are assembled into a prompt and sent to the local Ollama server running Llama 3.2 1B, which generates a grounded answer.
9. **Response** — The answer, along with cited source sections, is returned to the frontend and displayed to the user.

---

## 🚀 Running Locally

### Prerequisites
- Python 3.10+
- [Ollama](https://ollama.com) installed locally
- Docker (optional, for containerized run)

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/ai-research-mentor.git
cd ai-research-mentor
```

### 2. Backend setup
```bash
pip install -r requirements.txt

# Pull the local model
ollama pull llama3.2:1b

# Start Ollama server
ollama serve &

# Start the FastAPI backend
uvicorn app:app --host 0.0.0.0 --port 7860
```

### 3. Frontend setup
In a separate environment (frontend only needs `streamlit` and `requests`):
```bash
pip install streamlit requests
streamlit run streamlit_app.py
```

Update `BACKEND_URL` in `streamlit_app.py` to point to your local backend (`http://127.0.0.1:7860`) when running locally.

---

## ☁️ Deployment

This project is deployed as **two separate services**, each with its own dependencies — this separation matters, since the backend's heavy ML dependencies (torch, ChromaDB, sentence-transformers) have no place in the lightweight frontend environment.

### Backend — Hugging Face Spaces (Docker, free CPU tier)
- Deployed via a `Dockerfile` that installs Ollama and its runner binaries, pulls the Llama 3.2 1B model at container startup, and serves the FastAPI app with Uvicorn on port `7860`.
- `entrypoint.sh` handles: starting the Ollama server → waiting until it's ready → pulling the model → launching Uvicorn.
- Runs entirely on free compute; no GPU required.

### Frontend — Streamlit Community Cloud
- Deployed from `streamlit_app.py`, pointed at the backend's public HF Space URL.
- Uses its own minimal `requirements.txt` (`streamlit`, `requests`) — kept separate from the backend's dependency file to avoid unnecessary/conflicting installs.

---

## 🔌 API Reference

### `POST /upload-paper/`
Uploads and indexes a PDF.

**Request:** `multipart/form-data` with a `file` field (PDF only).

**Response:**
```json
{
  "status": "success",
  "message": "'paper.pdf' processed and indexed successfully."
}
```

### `POST /ask/`
Asks a question against the currently indexed paper(s).

**Request:**
```json
{
  "question": "What are the key concepts discussed in this paper?"
}
```

**Response:**
```json
{
  "question": "...",
  "answer": "...",
  "sources": [
    { "document": "paper", "section": "methodology", "chunk_index": 2 }
  ]
}
```

---

## ⚠️ Known Limitations

- **Free-tier cold starts:** Since the backend runs on Hugging Face's free CPU tier with no persistent storage, the Llama model is re-downloaded on every cold start (sleep/wake or rebuild), which adds startup latency.
- **CPU-only inference:** No GPU acceleration on the free tier — response times are slower than a hosted API would provide, especially for longer documents.
- **1B parameter model:** Llama 3.2 1B is small and fast enough to run on free CPU infrastructure, but has less reasoning depth than larger models — a deliberate trade-off for zero-cost, fully local operation.
- **Ephemeral vector storage:** Indexed papers do not persist across backend restarts; users need to re-upload after a cold start.

---

## 🗺️ Roadmap

- [ ] Persistent vector storage across restarts
- [ ] Bake the LLM into the Docker image to eliminate runtime download latency
- [ ] Support multi-paper comparison
- [ ] Add reranking to improve retrieval precision
- [ ] Support larger/alternate local models as configurable options

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to open an issue or submit a pull request.



---

*Built with a focus on being genuinely free to run — local inference, no API keys, no recurring costs.*




---
title: AI Research Mentor
emoji: 📄
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# AI Research Mentor Backend
FastAPI multi-document RAG backend engine.
