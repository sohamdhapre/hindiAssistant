import joblib
import numpy as np

model = joblib.load("intentModel.joblib")
vectorizer = joblib.load("intentVectorizer.joblib")

feature_names = vectorizer.get_feature_names_out()
weights = model.coef_

for i, intent in enumerate(model.classes_):
    print("\nIntent:", intent)

    top = np.argsort(weights[i])[-10:]

    for idx in reversed(top):
        print(feature_names[idx], weights[i][idx])
