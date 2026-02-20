
def tokenize(text: str)-> list:

    if text is None:
        return []
    
    tokens = text.split(" ")

    tokens = [t for t in tokens if t]

    return tokens
