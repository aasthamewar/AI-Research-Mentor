def rerank_chunks(query, retrieved_chunks, retrieved_metadata):
    # 1. Define common words to ignore (Stopwords)
    stopwords = {"what", "is", "are", "the", "a", "an", "and", "or", "in", "of", "to", "for", "with", "why"}
    
    # 2. Extract unique, meaningful keywords from the query
    query_words = [word.lower() for word in query.split() if word.lower() not in stopwords]
    
    # If the query only contained stopwords, fallback to using all words
    if not query_words:
        query_words = [word.lower() for word in query.split()]

    scored_pairs = []

    # 3. Zip chunks and metadata together so they stay locked in sync
    for chunk, metadata in zip(retrieved_chunks, retrieved_metadata):
        chunk_lower = chunk.lower()
        score = 0

        # Score based on meaningful keywords
        for word in query_words:
            score += chunk_lower.count(word)

        scored_pairs.append((score, chunk, metadata))

    # 4. Sort based on the score (highest score first)
    scored_pairs.sort(reverse=True, key=lambda x: x[0])

    # 5. Unpack them back into separate, matching lists
    reranked_chunks = [item[1] for item in scored_pairs]
    reranked_metadata = [item[2] for item in scored_pairs]

    return reranked_chunks, reranked_metadata