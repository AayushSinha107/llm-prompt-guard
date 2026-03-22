from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os

# 1. Initialize FastAPI
app = FastAPI(title="LLM Prompt Guard 🛡️")

# 2. Load the "Brain" and the "Translator"
MODEL_PATH = "models/firewall_model.pkl"
VECTORIZER_PATH = "models/tfidf_vectorizer.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise RuntimeError("Model files not found! Run train_model.py first.")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

# 3. Define the request structure
class PromptRequest(BaseModel):
    text: str

# 4. The Prediction Endpoint
@app.post("/check-prompt")
async def check_prompt(request: PromptRequest):
    # Convert text to the mathematical format the model understands
    tfidf_input = vectorizer.transform([request.text])
    
    # Predict (0 = Safe, 1 = Injection)
    prediction = model.predict(tfidf_input)[0]
    probability = model.predict_proba(tfidf_input)[0] # Confidence scores

    if prediction == 1:
        return {
            "status": "BLOCKED",
            "reason": "Potential Prompt Injection detected",
            "confidence": round(float(probability[1]) * 100, 2)
        }
    
    return {
        "status": "CLEAN",
        "message": "Prompt is safe to send to LLM",
        "confidence": round(float(probability[0]) * 100, 2)
    }

@app.get("/")
def home():
    return {"message": "Firewall is active and standing guard."}