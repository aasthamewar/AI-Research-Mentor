import os
import shutil
import gc
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# Import your core pipeline modules
from pdf_reader import extract_paper_text
from text_cleaner import clean_text
from section_parser import extract_sections  # Using your section-aware parser
from text_chunker import chunk_text
from embedding_generator import generate_embeddings
from vector_store import store_embeddings, search_similar_chunks
from reranker import rerank_chunks
from rag_pipeline import generate_rag_answer
from memory import add_to_memory

app = FastAPI(
    title="AI Research Mentor Backend")
# Ensure CORS is completely wide open to accept requests from Streamlit Cloud
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure a temporary directory exists to hold uploaded papers if needed
UPLOAD_DIR = "papers"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    question: str


# ---------------- 1. UPLOAD & INDEX ENDPOINT ----------------
@app.post("/upload-paper/")
async def upload_paper(file: UploadFile = File(...)):
    """
    Receives a PDF file, saves it, cleans it, parses it by sections, 
    chunks it, and saves the vectors into ChromaDB.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        # Save the uploaded file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print(f"\nProcessing upload: {file.filename}")

        # 1. Extract and Clean
        text = extract_paper_text(file_path)
        text = clean_text(text)

        # 2. Section-Aware Parsing
        sections = extract_sections(text)

        all_chunks = []
        all_metadata = []
        document_name = file.filename.replace(".pdf", "")

        # 3. Process each section individually
        for section_name, section_content in sections.items():
            section_chunks = chunk_text(section_content)
            
            for idx, chunk_text_block in enumerate(section_chunks):
                all_chunks.append(chunk_text_block)
                all_metadata.append({
                    "document": document_name,
                    "section": section_name,
                    "chunk_index": idx
                })

        if not all_chunks:
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")

        # 4. Generate Embeddings & Store
        embeddings = generate_embeddings(all_chunks)
        store_embeddings(all_chunks, embeddings, document_name, all_metadata)

        # 5. Clean up RAM instantly
        del text, sections, all_chunks, embeddings, all_metadata
        gc.collect()

        return {"status": "success", "message": f"'{file.filename}' processed and indexed successfully."}

    except Exception as e:
        # Clean up file if something goes wrong mid-process
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing document: {str(e)}")


# ---------------- 2. CONVERSATIONAL QUERY ENDPOINT ----------------
@app.post("/ask/")
def ask_question(request: QueryRequest):
    """
    Takes a query, retrieves context from ChromaDB, reranks it,
    generates an answer with Llama 3.2, and updates context memory.
    """
    query = request.question

    try:
        # 1. Retrieve raw chunks from ChromaDB (Pull top 5 or 6)
        results = search_similar_chunks(query, n_results=6)
        
        if not results or not results['documents'] or not results['documents'][0]:
            return {
                "question": query,
                "answer": "No relevant documents have been uploaded or found for this query.",
                "sources": []
            }

        initial_chunks = results['documents'][0]
        initial_metadata = results['metadatas'][0]

        # 2. Rerank (Fixed: capturing both return parameters to prevent ValueError)
        retrieved_chunks, retrieved_metadata = rerank_chunks(
            query,
            initial_chunks,
            initial_metadata
        )

        # 3. Generate answer
        answer = generate_rag_answer(
            query,
            retrieved_chunks,
            retrieved_metadata
        )

        # 4. Store conversation memory
        add_to_memory(query, answer)

        # 5. Build source dict list matching your Streamlit frontend's expectations
        sources = []
        for metadata in retrieved_metadata:
            sources.append({
                "document": metadata.get("document", "Unknown"),
                "section": metadata.get("section", "General"),
                "chunk_index": metadata.get("chunk_index", 0)
            })

        return {
            "question": query,
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Engine Error: {str(e)}")