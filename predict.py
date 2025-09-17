import pickle

def predict_severity(description):
    model = pickle.load(open("model.pkl", "rb"))
    vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
    X = vectorizer.transform([description])
    return model.predict(X)[0]

