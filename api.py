from fastapi import FastAPI, HTTPException
from pdf_reader import extract_paper_text
from ai_explainer import explain_research_paper
from paper_parser import extract_abstract 
import re

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Research Paper MCP API Running"}

@app.get("/explain-paper")
def explain_paper(filepath: str = "papers/paper1.pdf"):
    try:
        # 1. Extract text from the provided filepath
        text = extract_paper_text(filepath)
        
        abstract = extract_abstract(text)
        
        explanation = explain_research_paper(abstract[:2000])
        
        return {
            "filename": filepath,
            "explanation": explanation
        }
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="PDF file not found at the specified path.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))