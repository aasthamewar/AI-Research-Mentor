import ollama
import json
from prompts import research_explanation_prompt
def explain_research_paper(content):
    prompt = research_explanation_prompt(content)
    
    try:
        response = ollama.chat(
            model='phi3:mini',
            messages=[{'role': 'user', 'content': prompt}],
            format='json'
        )
        result_content = response['message']['content']
        return json.loads(result_content)
    except json.JSONDecodeError:
        return {"error": "Model generated invalid JSON", "raw": response['message']['content']}
    except Exception as e:
        return {"error": str(e)}