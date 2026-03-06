import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PredictionRequest(BaseModel):
    contact_email: str
    appointment_date: str
    appointment_value: float = 150.0
    days_since_scheduled: int = 7
    is_new_patient: bool = False
    previous_no_shows: int = 0
    lead_time_days: int = 14

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "No-Show Prediction API"}

@app.post("/predict")
def predict(request: PredictionRequest):
    prob = 0.2
    if request.previous_no_shows > 0:
        prob += request.previous_no_shows * 0.1
    if request.is_new_patient:
        prob += 0.15
    if request.lead_time_days > 14:
        prob += 0.1
    
    if prob >= 0.5:
        risk = "HIGH"
    elif prob >= 0.3:
        risk = "MEDIUM"
    else:
        risk = "LOW"
    
    return {
        "contact_email": request.contact_email,
        "no_show_probability": round(prob * 100, 1),
        "risk_level": risk,
        "revenue_at_risk": round(request.appointment_value * prob, 2)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
