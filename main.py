import os
import sys
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import HubSpot integration
try:
    from integrations import HubSpotClient, NoShowROIIntegration
    HUBSPOT_AVAILABLE = True
except ImportError:
    HUBSPOT_AVAILABLE = False

app = FastAPI(
    title="No-Show Prediction API",
    description="No-show prediction with HubSpot integration",
    version="2.0.0"
)

class PredictionRequest(BaseModel):
    contact_email: str
    appointment_date: str
    appointment_value: float = 150.0
    days_since_scheduled: int = 7
    is_new_patient: bool = False
    previous_no_shows: int = 0
    lead_time_days: int = 14
    hour_of_day: Optional[int] = 9

def calculate_prediction(request):
    """Rule-based prediction"""
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
        "version": "2.0.0",
        "hubspot_integration": HUBSPOT_AVAILABLE
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
