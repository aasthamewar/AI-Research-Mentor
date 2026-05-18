import os
import gc

from pdf_reader import extract_paper_text
from ai_explainer import explain_research_paper
from text_chunker import chunk_text
from paper_parser import extract_abstract
from embedding_generator import generate_embeddings
from vector_store import store_embeddings, search_similar_chunks, reset_collection
from rag_pipeline import generate_rag_answer
from text_cleaner import clean_text
from reranker import rerank_chunks
from memory import add_to_memory


papers_folder = "papers"

# Track totals across documents safely
total_docs_processed = 0
total_chunks_stored = 0

reset_collection()

for filename in os.listdir(papers_folder):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(papers_folder, filename)
        print(f"\nProcessing: {filename}")

        # 1. Extract and Clean
        text = extract_paper_text(pdf_path)
        text = clean_text(text)
        
        # 2. Chunk
        chunks = chunk_text(text)
        total_chunks_stored += len(chunks)
        total_docs_processed += 1
        
        # 3. Embed
        embeddings = generate_embeddings(chunks)
        
        # 4. Save
        document_name = filename.replace(".pdf", "")
        store_embeddings(chunks, embeddings, document_name)
        
        # 5. Instantly clear RAM for next iteration
        del text, chunks, embeddings
        gc.collect()

print(f"\n--- Processing Complete ---")
print(f"Total Documents: {total_docs_processed}")
print(f"Total Chunks Stored: {total_chunks_stored}")

# step 7: Ask semantic query
query = input("\nAsk your research question: ")
results = search_similar_chunks(query)

# step 8: show retrieved chunks
print("\nRETRIEVED CHUNKS WITH METADATA:\n")

retrieved_chunks = results['documents'][0]
retrieved_metadata = results['metadatas'][0] 

retrieved_chunks, retrieved_metadata = rerank_chunks(
    query, 
    retrieved_chunks, 
    retrieved_metadata
)

for i, chunk in enumerate(retrieved_chunks):
    metadata = retrieved_metadata[i]
    print(f"\n--- RESULT {i+1} ---")
    print(f"Document: {metadata['document']}")
    print(f"Chunk Index: {metadata['chunk_index']}\n")
    print(chunk[:500])
    

   
# step 9: generate grounded answer
answer = generate_rag_answer(query, retrieved_chunks, retrieved_metadata)
print("\nFinal Rag answer:")
print(answer)
add_to_memory(query, answer)