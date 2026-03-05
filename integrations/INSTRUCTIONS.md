# Integration Instructions

## Setup

1. Install dependencies:
   pip install requests python-dotenv

2. Update main.py:
   from integrations import hubspot_router, roi_router
   app.include_router(hubspot_router, prefix="/api/v1")
   app.include_router(roi_router, prefix="/api/v1")

3. Configure:
   Copy .env.integrations to .env and add your HubSpot API key

## API Endpoints

HubSpot:
- POST /api/v1/hubspot/sync-patient
- GET /api/v1/hubspot/high-risk-patients
- POST /api/v1/hubspot/update-outcome

ROI Calculator:
- POST /api/v1/roi/calculate
- GET /api/v1/roi/scenarios
