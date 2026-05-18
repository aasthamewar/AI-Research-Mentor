import re


def extract_abstract(text):

    # Standard abstract extraction
    abstract_match = re.search(
        r'abstract[:\s]*(.*?)(?:\bindex terms\b|\bkeywords\b|[1I]\.\s+introduction)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if abstract_match:

        return abstract_match.group(1).strip()

    # Fallback extraction
    fallback_match = re.search(
        r'(?:[\w\.-]+@[\w\.-]+\.\w+)(.*?)(?:[1I]\.\s+introduction)',
        text,
        re.IGNORECASE | re.DOTALL
    )

    if fallback_match:

        return fallback_match.group(1).strip()

    # Final fallback
    return text[:2000]