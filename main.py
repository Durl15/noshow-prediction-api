import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(
    title="No-Show Prediction API",
    version="2.0.0"
)

class PredictionRequest(BaseModel):
    contact_email: str = Field(..., description="Contact email address")
    appointment_date: str = Field(..., description="Appointment date YYYY-MM-DD")
    appointment_value: float = Field(default=150.0, description="Appointment value in USD")
    days_since_scheduled: int = Field(default=7, description="Days since appointment was scheduled")
    is_new_patient: bool = Field(default=False, description="Is this a new patient")
    previous_no_shows: int = Field(default=0, description="Number of previous no-shows")
    lead_time_days: int = Field(default=14, description="Lead time in days")
    hour_of_day: Optional[int] = Field(default=9, description="Hour of appointment")

def calculate_prediction(request: PredictionRequest) -> float:
    prob = 0.2
    if request.previous_no_shows > 0:
        prob += request.previous_no_shows * 0.1
    if request.is_new_patient:
        prob += 0.15
    if request.lead_time_days > 14:
        prob += 0.1
    try:
        day = datetime.strptime(request.appointment_date, "%Y-%m-%d").weekday()
        if day >= 5:
            prob += 0.1
    except:
        pass
    return min(prob, 0.95)

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "No-Show Prediction API",
        "version": "2.0.0"
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    prob = calculate_prediction(request)
    if prob >= 0.5:
        risk = "HIGH"
        rec = "URGENT: Call to confirm + offer reschedule"
    elif prob >= 0.3:
        risk = "MEDIUM"
        rec = "Send SMS reminder 24hrs + email 48hrs before"
    else:
        risk = "LOW"
        rec = "Standard email reminder"
    
    return {
        "contact_email": request.contact_email,
        "no_show_probability": round(prob * 100, 1),
        "risk_level": risk,
        "revenue_at_risk": round(request.appointment_value * prob, 2),
        "recommendation": rec
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
