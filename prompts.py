def research_explanation_prompt(content):
    # Use the 'content' variable passed into the function
    if not content or len(content) < 50:
        return "Error: Could not extract enough content from the PDF to provide an explanation."
    
    prompt = f"""
    Act as a world-class research mentor. I will provide you with the Abstract/Introduction of a technical paper. 

    Your task is to:
    1. "THINK": Analyze the core problem the researchers are trying to solve.
    2. "SIMPLIFY": Explain the concept using a real-world analogy.
    3. "KEY TAKEAWAYS": List the 3 most important findings in bullet points.
    4. "CRITICAL CHALLENGE": Identify one major hurdle mentioned in the text.

    Structure your response clearly. Use beginner-friendly language.
    
    Use this exact JSON structure:

    {{
        "main_idea": "...",
        "real_world_analogy": "...",
        "key_takeaways": [
            "...",
            "...",
            "..."
        ],
        "applications": [
            "...",
            "..."
        ],
        "challenges": [
            "...",
            "..."
        ],
        "difficulty_level": "...",
        "why_this_research_matters": "..."
    }}

    PAPER CONTENT:
    {content}
    """
    print("Requesting explanation from DeepSeek (Ollama)...")
    return prompt