import re

def normalize(text:str) -> str:

    if text is None:
        return ""
    
    text = text.strip()
    text = text.lower()
    text = re.sub(r"[?!।.,]", "", text)
    text = re.sub(r"\s+", " ", text)

    return text

def normalizeNumbers(text: str) -> str:
    
    return re.sub(r'\b\d+\b', '', text)
