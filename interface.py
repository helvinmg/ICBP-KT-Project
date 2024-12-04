
import streamlit as st
import pandas as pd
import joblib

# Load the model from the .sav file
model = joblib.load("Models/general_model.sav")  # Replace with your model file path

# Function to predict disease
def predict_disease(temp_f, pulse_rate_bpm, vomiting, yellowish_urine, indigestion):
    try:
        # Prepare user input as a DataFrame
        user_input = pd.DataFrame({
            'Temp': [temp_f],
            'Pulserate': [pulse_rate_bpm],
            'Vomiting': [vomiting],
            'YellowishUrine': [yellowish_urine],
            'Indigestion': [indigestion]
        })

        # Check if the scaler is part of the loaded model and standardize if required
        if hasattr(model, 'transform'):
            # If a scaler is part of the model, standardize the input
            standardized_input = model.transform(user_input)
        else:
            standardized_input = user_input  # If no scaler, use raw input directly

        # Make prediction
        predicted_disease = model.predict(standardized_input)[0]
        return predicted_disease
    except Exception as e:
        return f"Error during prediction: {e}"

# Streamlit Interface
st.set_page_config(page_title="Disease Prediction", layout="wide")

# Main container
container = st.container()
with container:
    st.title("Disease Prediction System")
    st.subheader("Enter your medical details to predict the disease")

    # Sidebar for input collection
    with st.sidebar:
        st.title("User Inputs")
        temp_f = st.number_input("Temperature (°F):", min_value=90.0, max_value=110.0, value=98.6, step=0.1)
        pulse_rate_bpm = st.number_input("Pulse Rate (bpm):", min_value=40, max_value=180, value=75)
        

    # Button to predict disease
    if st.sidebar.button("Predict Disease"):
        prediction = predict_disease(temp_f, pulse_rate_bpm, vomiting, yellowish_urine, indigestion)
        st.success(f"Predicted Disease: {prediction}")

# Additional container content
with container:
    st.markdown("---")
    st.write("lorem ipsum")
    
    # Footer
    st.success("By HMG")
