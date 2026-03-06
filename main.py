import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="No-Show Prediction API", version="2.0.0")

# Add CORS middleware to allow browser requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
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

@app.post("/predict")
def predict(request: PredictionRequest):
    prob = 0.2
    if request.previous_no_shows > 0:
        prob += request.previous_no_shows * 0.1
    if request.is_new_patient:
        prob += 0.15
    if request.lead_time_days > 14:
        prob += 0.1
    
    try:
        from datetime import datetime
        day = datetime.strptime(request.appointment_date, "%Y-%m-%d").weekday()
        if day >= 5:
            prob += 0.1
    except:
        pass
    
    prob = min(prob, 0.95)
    
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
