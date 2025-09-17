import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

def train_model():
    conn = sqlite3.connect("bugs.db")
    df = pd.read_sql("SELECT description, severity FROM bugs", conn)
    conn.close()

    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df["description"])
    y = df["severity"]

    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)

    pickle.dump(model, open("model.pkl", "wb"))
    pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()
# ML training script
