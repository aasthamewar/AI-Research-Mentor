import chromadb

import os

os.makedirs("/tmp/chroma_db", exist_ok=True)
# Create ChromaDB client
client = chromadb.PersistentClient(path="/tmp/chroma_db")

# Create collection
collection = client.get_or_create_collection(
    name="research_papers"
)


def store_embeddings(chunks, embeddings, document_name, metadata):

    processed_embeddings = [
        emb.tolist() if hasattr(emb, "tolist") else emb
        for emb in embeddings
    ]

    collection.add(
        documents=chunks,
        embeddings=processed_embeddings,
        metadatas=metadata,
        ids=[
            f"{document_name}_chunk_{i}"
            for i in range(len(chunks))
        ]
    )

    print("\nEmbeddings stored successfully.")

def search_similar_chunks(query, n_results=5):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    return results

def reset_collection():

    global collection

    client.delete_collection("research_papers")

    collection = client.get_or_create_collection(
        name="research_papers"
    )

    print("\nCollection reset successfully.")