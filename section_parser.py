import re

# Better patterns that look for section titles near the beginning of lines or with numbers
SECTION_KEYWORDS = {
    "abstract": r"^\s*(?:abstract)\b",
    "introduction": r"^\s*(?:[i|v|x\d\.\-]+\s+)?(?:introduction)\b",
    "methodology": r"^\s*(?:[i|v|x\d\.\-]+\s+)?(?:methodology|methods|approach|system architecture|proposed framework)\b",
    "dataset": r"^\s*(?:[i|v|x\d\.\-]+\s+)?(?:dataset|data|experimental setup)\b",
    "results": r"^\s*(?:[i|v|x\d\.\-]+\s+)?(?:results|evaluation|experiments|performance)\b",
    "conclusion": r"^\s*(?:[i|v|x\d\.\-]+\s+)?(?:conclusion|discussion|summary)\b"
}

def extract_sections(text):
    # Split text into lines to inspect them as potential headers
    lines = text.split('\n')
    
    matches = []
    current_char_pos = 0
    
    for line in lines:
        line_len = len(line) + 1 # +1 accounts for the split '\n'
        line_lower = line.lower().strip()
        
        # Guard rails to avoid matching long normal sentences containing keywords
        if len(line_lower) < 100: 
            for section_name, pattern in SECTION_KEYWORDS.items():
                if re.search(pattern, line_lower):
                    matches.append((current_char_pos, section_name))
                    break # Stop checking other patterns for this specific line
                    
        current_char_pos += line_len

    # If absolutely no headings were found, fallback to treating the whole thing as 'general'
    if not matches:
        return {"general": text.strip()}

    # Sort matches by their position in the text
    matches.sort(key=lambda x: x[0])

    sections = {}
    
    # Capture anything before the first matched section (e.g., Title, Authors, Meta)
    if matches[0][0] > 0:
        sections["header_meta"] = text[0:matches[0][0]].strip()

    # Extract text slices dynamically between headers
    for i in range(len(matches)):
        start_pos, section_name = matches[i]
        
        end_pos = (
            matches[i + 1][0]
            if i + 1 < len(matches)
            else len(text)
        )
        
        section_text = text[start_pos:end_pos].strip()
        
        # If a section header is matched multiple times, append it rather than overwriting
        if section_name in sections:
            sections[section_name] += "\n\n" + section_text
        else:
            sections[section_name] = section_text

    return sections