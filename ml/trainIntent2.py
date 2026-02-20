import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.pipeline import Pipeline
from sklearn.utils import resample
import joblib
from nlp.normalizer import normalizeNumbers
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "intentData.csv"
MODEL_PATH = BASE_DIR /  "intentModel.joblib"
VEC_PATH = BASE_DIR /  "intentVectorizer.joblib"

def load_and_balance_data(csv_path):

    df = pd.read_csv(csv_path)
    
    df_math = df[df['intent'] == 'math']
    df_others = df[df['intent'] != 'math']
    

    if len(df_math) > 150:
        df_math = resample(df_math, 
                           replace=False, 
                           n_samples=150, 
                           random_state=42)
    
    df_balanced = pd.concat([df_others, df_math])
    
    print(f"Original Data Size: {len(df)}")
    print(f"Balanced Data Size: {len(df_balanced)}")
    print("Class Distribution:\n", df_balanced['intent'].value_counts())
    
    return df_balanced

def train():
    print("🚀 Loading and Balancing Data...")
    data = load_and_balance_data(DATA_PATH)
    
    X = data["text"].apply(normalizeNumbers)
    y = data["intent"]

    print("🧠 Training Advanced Model (LinearSVC + Char N-Grams)...")
    

    model_pipeline = Pipeline([
        ('vect', TfidfVectorizer(
            ngram_range=(2, 5),  
            analyzer="char_wb",  
            max_df=0.95,         
            min_df=2             
        )),
        ('clf', CalibratedClassifierCV(
            LinearSVC(C=1.0, max_iter=1000, dual="auto"),
            method='sigmoid'
        ))
    ])

    model_pipeline.fit(X, y)

    joblib.dump(model_pipeline.named_steps['vect'], VEC_PATH)
    joblib.dump(model_pipeline.named_steps['clf'], MODEL_PATH)

    print(f"Model saved to {MODEL_PATH}")
    print(f" Vectorizer saved to {VEC_PATH}")
    print("Training Complete")

if __name__ == "__main__":
    train()