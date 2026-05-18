import re


def clean_text(text):

    # Remove URLs
    text = re.sub(r'http\S+|www\S+', ' ', text)

    # Remove citation references like [25]
    text = re.sub(r'\[\d+\]', ' ', text)

    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)

    # Remove References section and everything after it
    references_match = re.split(
        r'\breferences\b',
        text,
        flags=re.IGNORECASE
    )

    text = references_match[0]

    return text.strip()