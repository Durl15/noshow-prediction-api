from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
import os
from datetime import datetime

router = APIRouter(prefix="/hubspot", tags=["hubspot"])

HUBSPOT_API_KEY = os.getenv("HUBSPOT_API_KEY", "")
BASE_URL = "https://api.hubapi.com"

class Patient(BaseModel):
    patient_id: str
    email: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    no_show_probability: float
    risk_level: str

@router.post("/sync-patient")
async def sync_patient(patient: Patient):
    if not HUBSPOT_API_KEY:
        raise HTTPException(500, "HUBSPOT_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    properties = {
        "email": patient.email,
        "firstname": patient.first_name,
        "lastname": patient.last_name,
        "phone": patient.phone or "",
        "no_show_risk_score": str(patient.no_show_probability),
        "risk_level": patient.risk_level,
        "last_synced": datetime.now().isoformat()
    }
    
    search_url = f"{BASE_URL}/crm/v3/objects/contacts/search"
    search_payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "email",
                "operator": "EQ",
                "value": patient.email
            }]
        }]
    }
    
    search = requests.post(search_url, headers=headers, json=search_payload)
    
    if search.status_code == 200:
        results = search.json().get("results", [])
        
        if results:
            contact_id = results[0]["id"]
            update_url = f"{BASE_URL}/crm/v3/objects/contacts/{contact_id}"
            requests.patch(update_url, headers=headers, json={"properties": properties})
            action = "updated"
        else:
            create_url = f"{BASE_URL}/crm/v3/objects/contacts"
            response = requests.post(create_url, headers=headers, json={"properties": properties})
            contact_id = response.json().get("id")
            action = "created"
        
        return {"status": "success", "action": action, "contact_id": contact_id}
    
    raise HTTPException(500, "HubSpot API error")

@router.get("/high-risk-patients")
async def get_high_risk(threshold: float = 0.7):
    if not HUBSPOT_API_KEY:
        raise HTTPException(500, "HUBSPOT_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {HUBSPOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "filterGroups": [{
            "filters": [{
                "propertyName": "no_show_risk_score",
                "operator": "GTE",
                "value": str(threshold)
            }]
        }],
        "properties": ["email", "firstname", "lastname", "no_show_risk_score", "risk_level"],
        "limit": 100
    }
    
    r = requests.post(f"{BASE_URL}/crm/v3/objects/contacts/search", headers=headers, json=payload)
    
    if r.status_code == 200:
        patients = []
        for res in r.json().get("results", []):
            p = res.get("properties", {})
            patients.append({
                "contact_id": res.get("id"),
                "email": p.get("email"),
                "first_name": p.get("firstname"),
                "last_name": p.get("lastname"),
                "no_show_probability": float(p.get("no_show_risk_score", 0)),
                "risk_level": p.get("risk_level")
            })
        return {"patients": patients, "count": len(patients)}
    
    raise HTTPException(500, "Failed to fetch from HubSpot")
