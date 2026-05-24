# AI Research Mentor

AI Research Mentor is an AI-powered research paper understanding system designed to help beginners understand complex research papers interactively.

Instead of overwhelming users with the entire paper at once, the system allows users to upload research papers and explore specific aspects such as:

- Beginner-friendly explanation
- Key concepts
- Methodology
- Architecture flow
- Dataset used
- Results and evaluation
- Research limitations

The system uses Retrieval-Augmented Generation (RAG), ChromaDB, local LLM inference with Ollama, and a Streamlit frontend.

## Below is the workflow
<img width="1536" height="1024" alt="AI_Research Diagram" src="https://github.com/user-attachments/assets/fadfc637-fcfd-4e84-b907-4952e81dd320" />


---

# Project Goal

Research papers are often difficult for:
- students
- beginners
- developers entering a new field

This project aims to bridge that gap by converting complex research papers into structured, interactive, beginner-friendly insights.

---

# Features

## Current Features

### Research Paper Upload
- Upload PDF research papers
- Automatic text extraction and processing

### Intelligent Processing Pipeline
- Text cleaning
- Chunking
- Section-aware parsing
- Embedding generation

### Vector Database Storage
- Persistent ChromaDB storage
- Semantic retrieval

### AI Research Assistant
Users can ask:
- "Explain this paper for beginners"
- "What dataset was used?"
- "What are the key concepts?"
- "What methodology is proposed?"
- "What are the limitations?"

### Conversational Memory
- Maintains conversation history
- Improves contextual responses

### Source Tracking
Each response includes:
- source paper
- section metadata

### Local LLM Inference
- Runs using Ollama
- Uses `llama3.2:1b`

### Frontend
- Streamlit-based UI
- Interactive research exploration

### Backend
- FastAPI-based backend API

### Docker Deployment
- Deployable on Hugging Face Spaces

---

# Tech Stack

## Frontend
- Streamlit

## Backend
- FastAPI

## LLM
- Ollama
- Llama 3.2 1B

## Vector Database
- ChromaDB

## Embeddings
- SentenceTransformers

## PDF Processing
- PyMuPDF

## Deployment
- Docker
- Hugging Face Spaces

---

# System Architecture

```text
User Uploads Paper
        ↓
PDF Extraction
        ↓
Text Cleaning
        ↓
Section Parsing
        ↓
Chunking
        ↓
Embedding Generation
        ↓
ChromaDB Storage
        ↓
Semantic Retrieval
        ↓
RAG Pipeline
        ↓
LLM Response Generation
        ↓
Frontend Display

```



---
title: AI Research Mentor Backend
emoji: 📘
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# AI Research Mentor Backend
FastAPI multi-document RAG backend engine.
