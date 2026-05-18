import fitz
import re

def extract_paper_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    
    for page in doc:
        # Using "blocks" can sometimes help preserve the order of text better
        text += page.get_text("text") + "\n"
        
    # Instead of replacing ALL whitespace with one space, 
    # let's just clean up multiple spaces/newlines into a single newline
    # This keeps the "sections" easier to find for the regex.
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r' +', ' ', text)
    
    return text