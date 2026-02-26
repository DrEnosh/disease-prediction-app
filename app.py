import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# --------------------- BEAUTIFUL UI ---------------------
st.set_page_config(page_title="Disease Prediction", layout="centered")

# --------------------- TRAIN & SAVE MODEL (runs only once) ---------------------
@st.cache_resource
def get_trained_model():
    # Load your Excel file (must be in the same folder)
    try:
        df = pd.read_excel('data01.xlsx')
    except FileNotFoundError:
        st.error("data01.xlsx not found! Please place it in the same folder as app.py")
        st.stop()

    # Basic cleaning
    df.drop_duplicates(inplace=True)

    # Remove outliers in age & BMI
    for col in ['age', 'BMI']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5*IQR) & (df[col] <= Q3 + 1.5*IQR)]

    # Handle missing values
    df = df.dropna(subset=['outcome'])
    df['Respiratory rate'] = df['Respiratory rate'].fillna(df['Respiratory rate'].mean())
    df.fillna(df.mean(numeric_only=True), inplace=True)

    # Normalize all features from column 3 onward (exactly like in Colab)
    df.iloc[:, 3:] = df.iloc[:, 3:].apply(lambda x: (x - x.min()) / (x.max() - x.min() + 1e-8))

    # Features and target
    X = df.drop(['outcome', 'group', 'ID'], axis=1)
    y = df['outcome']

    # Train Random Forest
    model = RandomForestClassifier(n_estimators=300, random_state=42)
    model.fit(X, y)

    # Save everything we need later
    package = {
        'model': model,
        'columns': X.columns.tolist(),
        'means': X.mean().to_dict()
    }
    with open('model.pkl', 'wb') as f:
        pickle.dump(package, f)

    return package

# Load the model (trains only the first time)
package = get_trained_model()
model = package['model']
columns = package['columns']
means = package['means']

# --------------------- BEAUTIFUL UI ---------------------
st.title("Disease Prediction")

st.write("Enter patient details below. The model uses real hospital data for accurate prediction.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age in years", min_value=1, max_value=120, value=41)
    bmi = st.number_input("BMI (kg/m²)", min_value=10.0, max_value=70.0, value=25.2, step=0.1)

with col2:
    gender = st.selectbox("Gender", ["Male", "Female"])
    hypertensive = st.selectbox("Hypertensive", ["No", "Yes"])
    atrial_fib = st.selectbox("Atrial Fibrillation", ["No", "Yes"])

# Convert to numbers
gender_val = 1 if gender == "Female" else 0
hypertensive_val = 1 if hypertensive == "Yes" else 0
atrial_fib_val = 1 if atrial_fib == "Yes" else 0

# Simple scaling (same ranges used in training)
age_scaled = (age - 18) / (90 - 18)
bmi_scaled = (bmi - 15) / (50 - 15)

st.markdown("### Scaled values used for prediction")
st.json({
    "age_scaled": round(age_scaled, 4),
    "bmi_scaled": round(bmi_scaled, 4),
    "gender (1=Female)": gender_val,
    "hypertensive": hypertensive_val,
    "atrial_fibrillation": atrial_fib_val
})

if st.button("Predict Outcome", type="primary", use_container_width=True):
    # Build full 48-feature vector
    row = []
    for col in columns:
        if col == "age":
            row.append(age_scaled)
        elif col == "gendera":
            row.append(gender_val)
        elif col == "BMI":
            row.append(bmi_scaled)
        elif col == "hypertensive":
            row.append(hypertensive_val)
        elif col == "atrialfibrillation":
            row.append(atrial_fib_val)
        else:
            row.append(means.get(col, 0.5))  # use average from training data

    # Predict
    pred = model.predict([row])[0]
    prob = model.predict_proba([row])[0][1]

    if pred == 1:
        st.error("HIGH RISK OF DISEASE")
        st.warning(f"Probability: {prob:.1%}")
    else:
        st.success("LOW RISK")
        st.info(f"Probability of disease: {prob:.1%}")

    st.balloons()