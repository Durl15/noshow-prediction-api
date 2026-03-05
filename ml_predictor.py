import joblib
import pandas as pd
from datetime import datetime
import os

class NoShowPredictor:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        model_path = os.path.join(os.path.dirname(__file__), 'no_show_model.pkl')
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            return True
        return False
    
    def predict(self, appointment_date, days_since_scheduled, is_new_patient, 
                previous_no_shows, appointment_value, lead_time_days, hour_of_day=None):
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            appt_date = datetime.strptime(appointment_date, "%Y-%m-%d")
            day_of_week = appt_date.weekday()
        except:
            day_of_week = 0
        
        if hour_of_day is None:
            hour_of_day = 9
        
        features = pd.DataFrame([{
            'day_of_week': day_of_week,
            'hour_of_day': hour_of_day,
            'days_since_scheduled': days_since_scheduled,
            'is_new_patient': int(is_new_patient),
            'previous_no_shows': previous_no_shows,
            'appointment_value': appointment_value,
            'lead_time_days': lead_time_days
        }])
        
        no_show_prob = self.model.predict_proba(features)[0][1]
        
        return {
            'no_show_probability': float(no_show_prob),
            'features_used': features.to_dict('records')[0]
        }
    
    def get_risk_level(self, probability):
        if probability >= 0.5:
            return "HIGH"
        elif probability >= 0.3:
            return "MEDIUM"
        else:
            return "LOW"
    
    def get_recommendation(self, risk_level, probability):
        recommendations = {
            "HIGH": "URGENT: Call to confirm + offer reschedule",
            "MEDIUM": "Send SMS reminder 24hrs + email 48hrs before",
            "LOW": "Standard email reminder"
        }
        return recommendations.get(risk_level, "Standard reminder")

predictor = NoShowPredictor()
