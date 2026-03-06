import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configure CORS - must be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

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

@app.options("/predict")
def predict_options():
    return {}

@app.post("/predict")
def predict(request: PredictionRequest):
    prob = 0.2
    if request.previous_no_shows > 0:
        prob += request.previous_no_shows * 0.1
    if request.is_new_patient:
        prob += 0.15
    if request.lead_time_days > 14:
        prob += 0.1
    
    prob = min(prob, 0.95)
    
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
        "revenue_at_risk": round(request.appointment_value * prob, 2),
        "recommendation": "Standard reminder"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
