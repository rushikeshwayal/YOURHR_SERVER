from fastapi import APIRouter, HTTPException
import joblib
import os

from ML.ResumeStrength.schemas.resume_strength import ResumeStrengthRequest

router = APIRouter(prefix="/resume-strength", tags=["Resume Strength"])

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Try expected location first
MODEL_DIR = os.path.join(CURRENT_DIR, "..", "model")

MODEL_PATH = os.path.join(MODEL_DIR, "resume_shortlist_model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

print("Looking for model at:", MODEL_PATH)
print("Exists:", os.path.exists(MODEL_PATH))

if not os.path.exists(MODEL_PATH):
    raise RuntimeError("❌ resume_shortlist_model.pkl not found")

if not os.path.exists(SCALER_PATH):
    raise RuntimeError("❌ scaler.pkl not found")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

EDUCATION_MAP = {
    "High School": 1,
    "Bachelors": 2,
    "Masters": 3,
    "PhD": 4
}

@router.post("/predict")
def predict_resume_strength(payload: ResumeStrengthRequest):
    try:
        # Encode education
        education_encoded = EDUCATION_MAP[payload.education_level]

        # Feature vector (ORDER MATTERS!)
        features = [[
            payload.years_experience,
            payload.skills_match_score,
            education_encoded,
            payload.project_count,
            payload.github_activity
        ]]

        # Scale features
        features_scaled = scaler.transform(features)

        # Predict probability
        probability = model.predict_proba(features_scaled)[0][1]

        # Convert to score
        strength_score = round(probability * 100, 2)

        return {
            "resume_strength_score": strength_score,
            "probability": round(probability, 4),
            "confidence_level": (
                "High" if strength_score >= 75
                else "Medium" if strength_score >= 50
                else "Low"
            )
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
