import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

np.random.seed(42)
n_samples = 2000

data = {
    'day_of_week': np.random.randint(0, 7, n_samples),
    'hour_of_day': np.random.randint(8, 18, n_samples),
    'days_since_scheduled': np.random.randint(0, 30, n_samples),
    'is_new_patient': np.random.randint(0, 2, n_samples),
    'previous_no_shows': np.random.randint(0, 6, n_samples),
    'appointment_value': np.random.randint(50, 500, n_samples),
    'lead_time_days': np.random.randint(1, 60, n_samples),
}

df = pd.DataFrame(data)

# Create target with strong signals
no_show_prob = (
    (df['day_of_week'] >= 5) * 0.25 +
    (df['is_new_patient']) * 0.20 +
    (df['previous_no_shows'] * 0.15) +
    (df['lead_time_days'] > 14) * 0.15 +
    np.random.random(n_samples) * 0.25
)

df['no_show'] = (no_show_prob > 0.6).astype(int)

X = df.drop('no_show', axis=1)
y = df['no_show']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)

print(f"Accuracy: {model.score(X_test, y_test):.2f}")

# Test predictions
test_cases = pd.DataFrame([
    {'day_of_week': 1, 'hour_of_day': 9, 'days_since_scheduled': 5, 'is_new_patient': 0, 'previous_no_shows': 0, 'appointment_value': 200, 'lead_time_days': 7},
    {'day_of_week': 6, 'hour_of_day': 9, 'days_since_scheduled': 2, 'is_new_patient': 1, 'previous_no_shows': 4, 'appointment_value': 300, 'lead_time_days': 30},
])

probs = model.predict_proba(test_cases)
print(f"Low risk: {probs[0][1]:.2%}")
print(f"High risk: {probs[1][1]:.2%}")

joblib.dump(model, 'no_show_model.pkl')
print("Model saved!")
