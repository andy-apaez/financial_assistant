import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib


class TransactionCategorizer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.model = MultinomialNB()

    def train(self, csv_file):
        df = pd.read_csv(csv_file)
        X = self.vectorizer.fit_transform(df["description"])
        y = df["category"]
        self.model.fit(X, y)
        joblib.dump((self.vectorizer, self.model), "data/trained_model.pkl")

    def predict(self, text):
        vectorizer, model = joblib.load("data/trained_model.pkl")
        X = vectorizer.transform([text])
        return model.predict(X)[0]


# Example usage
if __name__ == "__main__":
    cat = TransactionCategorizer()
    cat.train("data/sample.csv")
    print(cat.predict("Starbucks Coffee"))
