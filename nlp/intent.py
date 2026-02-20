
INTENT_PATTERNS = {
    "greeting": ["नमस्ते", "नमस्कार", "हैलो", "हाय"],
    "identity": ["कौन", "हो", "क्या"],
    "time": ["समय", "टाइम", "बजे", "alarm", "timer", "date"],
    "math": ["add, sub , mul , dvd"],
    "exit": ["बंद", "अलविदा", "exit"]

    # Temperature
    # Lights
}

#primitive

def classifyIntent(tokens: list) -> str:


    for intent, keywords in INTENT_PATTERNS.items():
        for kw in keywords:
            if kw in tokens:
                return intent

    return "unknown"
