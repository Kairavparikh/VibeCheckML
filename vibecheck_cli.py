import sys
import pickle
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python vibecheck_cli.py <text>")
        sys.exit(1)
    text = sys.argv[1]
    with open('sentiment_classifier.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    print(f"Sentiment: {pred}")

if __name__ == "__main__":
    main() 