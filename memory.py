conversation_history = []


def add_to_memory(query, answer):

    conversation_history.append({
        "query": query,
        "answer": answer
    })


def get_memory_context(limit=3):

    recent_conversations = conversation_history[-limit:]

    memory_text = ""

    for convo in recent_conversations:

        memory_text += (
            f"User Question: {convo['query']}\n"
        )

        memory_text += (
            f"Assistant Answer: {convo['answer']}\n\n"
        )

    return memory_text