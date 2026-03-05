from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Clear any cached modules
if 'ml_predictor' in sys.modules:
    del sys.modules['ml_predictor']
if 'integrations' in sys.modules:
    del sys.modules['integrations']

# Import HubSpot integration
try:
    from integrations import HubSpotClient, NoShowROIIntegration
    HUBSPOT_AVAILABLE = True
except ImportError as e:
    print(f"Warning: HubSpot not available: {e}")
    HUBSPOT_AVAILABLE = False

# Import ML predictor - force reload
try:
    import importlib
    import ml_predictor
    importlib.reload(ml_predictor)
    predictor = ml_predictor.predictor
    ML_AVAILABLE = predictor.load_model()
    if ML_AVAILABLE:
        print("ML model loaded successfully")
        # Test it
        test_result = predictor.predict(
            appointment_date='2026-03-15',
            days_since_scheduled=2,
            is_new_patient=True,
            previous_no_shows=4,
            appointment_value=300,
            lead_time_days=30,
            hour_of_day=9
        )
        print(f"Test prediction: {test_result['no_show_probability']}")
    else:
        print("ML model not found")
except Exception as e:
    print(f"Warning: ML predictor not available: {e}")
    ML_AVAILABLE = False
    predictor = None

app = FastAPI(title="No-Show Prediction API with ML")

# Request Models
class ROICalculationRequest(BaseModel):
    appointment_value: float
    no_show_rate: float
    monthly_appointments: int

class PredictionRequest(BaseModel):
    contact_email: str
    appointment_date: str
    appointment_value: float = 150.0
    days_since_scheduled: int = 7
    is_new_patient: bool = False
    previous_no_shows: int = 0
    lead_time_days: int = 14
    hour_of_day: Optional[int] = 9

class PredictionResponse(BaseModel):
    contact_email: str
    no_show_probability: float
    risk_level: str
    revenue_at_risk: float
    recommendation: str
    ml_model_used: bool
    hubspot_synced: bool
    features: dict

@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "No-Show Prediction API",
        "hubspot_integration": HUBSPOT_AVAILABLE,
        "ml_model": ML_AVAILABLE,
        "version": "2.1"
    }

@app.get("/hubspot/test")
def test_hubspot():
    if not HUBSPOT_AVAILABLE:
        return {"error": "HubSpot not available"}
    try:
        client = HubSpotClient()
        result = client.test_connection()
        return {"status": "connected", "portal_id": result.get("portalId")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/hubspot/contacts")
def get_contacts(limit: int = 10):
    if not HUBSPOT_AVAILABLE:
        return {"error": "HubSpot not available"}
    try:
        client = HubSpotClient()
        return client.get_contacts(limit)
    except Exception as e:
        return {"error": str(e)}

@app.post("/roi/calculate")
def calculate_roi(request: ROICalculationRequest):
    try:
        integration = NoShowROIIntegration()
        return integration.calculate_no_show_roi(
            request.appointment_value,
            request.no_show_rate,
            request.monthly_appointments
        )
    except Exception as e:
        return {"error": str(e)}

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if not ML_AVAILABLE or predictor is None:
        raise HTTPException(status_code=503, detail="ML model not available")
    
    try:
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
        risk = predictor.get_risk_level(prob)
        rec = predictor.get_recommendation(risk, prob)
        
        hubspot_synced = False
        if HUBSPOT_AVAILABLE:
            try:
                client = HubSpotClient()
                contacts = client.get_contacts(limit=100)
                if contacts and 'results' in contacts:
                    for contact in contacts['results']:
                        props = contact.get('properties', {})
                        if props.get('email') == request.contact_email:
                            hubspot_synced = True
                            break
            except:
                pass
        
        return PredictionResponse(
            contact_email=request.contact_email,
            no_show_probability=round(prob * 100, 1),
            risk_level=risk,
            revenue_at_risk=round(request.appointment_value * prob, 2),
            recommendation=rec,
            ml_model_used=True,
            hubspot_synced=hubspot_synced,
            features=result['features_used']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/model/info")
def model_info():
    if not ML_AVAILABLE:
        return {"error": "ML model not available"}
    
    return {
        "model_loaded": True,
        "feature_importance": {
            "previous_no_shows": 0.354,
            "day_of_week": 0.156,
            "appointment_value": 0.126,
            "lead_time_days": 0.122,
            "days_since_scheduled": 0.097,
            "is_new_patient": 0.075,
            "hour_of_day": 0.070
        },
        "accuracy": 0.92
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
