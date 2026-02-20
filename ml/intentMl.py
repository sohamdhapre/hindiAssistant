import joblib

vectorizer = joblib.load("ml/intentVectorizer.joblib")
model = joblib.load("ml/intentModel.joblib")

confidenceThreshold = 0.65

def classifyIntentML(text: str) -> str:

    if not text:
        return "unknown"

    X = vectorizer.transform([text])
    
    probs = model.predict_proba(X)[0]
    
    max_index = probs.argmax()      
    confidence = probs[max_index]   
    intent = model.classes_[max_index]
    
    if confidence < confidenceThreshold:
        return "unknown"
    
    return intent