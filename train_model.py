import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_firewall():
    # 1. Load the data you downloaded earlier
    if not os.path.exists('data/prompt_injections.csv'):
        print("❌ Error: CSV not found. Run download_data.py first.")
        return

    df = pd.read_csv('data/prompt_injections.csv')

    # 2. Preprocessing
    # We use the 'text' column as input and 'label' as output (1=Malicious, 0=Safe)
    X = df['text'].astype(str)
    y = df['label']

    # 3. Split data (80% training, 20% testing)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 4. Feature Extraction (Convert text to numbers)
    # Tfidf counts word importance. max_features=5000 keeps it lightweight.
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    # 5. Train the Model
    print("🚀 Training the Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_tfidf, y_train)

    # 6. Evaluate
    y_pred = model.predict(X_test_tfidf)
    print("\n--- Model Performance ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(classification_report(y_test, y_pred))

    # 7. Save the Model and Vectorizer
    if not os.path.exists('models'):
        os.makedirs('models')

    joblib.dump(model, 'models/firewall_model.pkl')
    joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
    
    print("\n✅ Success! Model saved in 'models/' folder.")

if __name__ == "__main__":
    train_firewall()