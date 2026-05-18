import ollama
from memory import get_memory_context

def generate_rag_answer(query, retrieved_chunks, retrieved_metadata):

    # Build source-aware retrieval context
    formatted_chunks = []

    for i, chunk in enumerate(retrieved_chunks):

        metadata = retrieved_metadata[i]

        # source_info = (
        #     f"Source: {metadata['document']}"
        # )
        # Pulling the parsed section name dynamically if available
        
        section_info = f" | Section: {metadata.get('section', 'General')}"
        source_info = f"Source: {metadata['document']}{section_info}"

        formatted_chunk = (
            f"{source_info}\n{chunk[:700]}"
        )

        formatted_chunks.append(formatted_chunk)

    context = "\n\n".join(formatted_chunks)
    
    memory_context = get_memory_context()
    
    extra_instructions = ""
    is_flow_request = any(word in query.lower() for word in ['flow', 'architecture', 'workflow', 'system', 'proposed'])
    
    from_key_sections = any(
        meta.get('section', '').lower() in ['methodology', 'architecture flow', 'proposed framework', 'system architecture'] 
        for meta in retrieved_metadata
    )
    
    if is_flow_request and from_key_sections:
        system_instruction += """
        
        CRITICAL: The user has requested a flow description or architecture diagram.
        Based ONLY on the CONTEXT, synthesize the step-by-step process described.
        Then, generate a Mermaid.js diagram representing this workflow.
        Structure your response exactly as follows:
        ### Step-by-Step Architecture Flow:
        [Detailed numbered list of steps]
        ### Workflow Diagram:
        ```mermaid
        [Generated Mermaid.js diagram code]
        ```
        """

    # context1 = f"""
    # Previous Conversation:

    # {memory_context}

    # Retrieved Research Context:

    # {context}
    # """

    prompt = f"""
    You are an AI research assistant.

    Answer the user's question ONLY using the provided context.

    If the answer is not present in the context, say:
    "The information is not available in the retrieved context."
    {extra_instructions}
    
    
    
    Retrieved Research Context:
    {context}

    USER QUESTION:
    {query}

    
    """
    

    response = ollama.chat(
        model='llama3.2:1b',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )

    return response['message']['content']