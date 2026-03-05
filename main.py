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

# Try to load ML model, fallback to rule-based if not available
try:
    from ml_predictor import predictor
    ML_AVAILABLE = predictor.load_model()
except Exception:
    ML_AVAILABLE = False
    predictor = None

app = FastAPI(
    title="No-Show Prediction API",
    description="ML-powered no-show prediction with HubSpot integration",
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

def rule_based_prediction(request):
    """Fallback rule-based prediction when ML model isn't available"""
    prob = 0.2  # Base 20%
    
    # Add risk factors
    if request.previous_no_shows > 0:
        prob += request.previous_no_shows * 0.1
    if request.is_new_patient:
        prob += 0.15
    if request.lead_time_days > 14:
        prob += 0.1
    
    # Day of week (weekends higher)
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
        "hubspot_integration": HUBSPOT_AVAILABLE,
        "ml_model": ML_AVAILABLE
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    try:
        if ML_AVAILABLE and predictor:
            # Use ML model
            result = predictor.predict(
                appointment_date=request.appointment_date,
                days_since_scheduled=request.days_since_scheduled,
                is_new_patient=request.is_new_patient,
                previous_no_shows=request.previous_no_shows,
                appointment_value=request.appointment_value,
                lead_time_days=request.lead_time_days,
                hour_of_day=request.hour_of_day
            )
            prob = result['no_show_probability']
            model_used = True
        else:
            # Use rule-based fallback
            prob = rule_based_prediction(request)
            model_used = False
        
        # Determine risk level
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
            "recommendation": rec,
            "ml_model_used": model_used
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
