import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from PIL import Image

st.markdown("""
    <style>
        .sidebar .sidebar-content {
            background-color: black;
            }
            footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            text-align: center;
            padding: 10px;
            background-color: #f0f8ff;
            font-size: 16px;
            color: #000;
        }
        
    </style>
    """, unsafe_allow_html=True)

# Load and preprocess the dataset
dataset = pd.read_csv("datasets/general.csv")
X = dataset.drop('Disease', axis=1)
y = dataset['Disease']
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Load the saved models
diabetes_model = pickle.load(open('Models/diabetes_model.sav', 'rb'))
heart_disease_model = pickle.load(open('Models/heart_disease_model1.sav', 'rb'))
parkinsons_model = pickle.load(open('Models/parkinsons_model.sav', 'rb'))

def predict_disease(temp_f, pulse_rate_bpm, vomiting, yellowish_urine, indigestion):
    # Prepare user input as a single-row DataFrame
    user_input = pd.DataFrame({
        'Temp': [temp_f],
        'Pulserate': [pulse_rate_bpm],
        'Vomiting': [vomiting],
        'YellowishUrine': [yellowish_urine],
        'Indigestion': [indigestion]
    })

    # Standardize the user input
    user_input = scaler.transform(user_input)

    # Make prediction
    predicted_disease = model.predict(user_input)[0]
    disease_names = { 0: 'Heart Disease', 1: 'Viral Fever/Cold', 2: 'Jaundice', 3: 'Food Poisoning', 4: 'Normal'}
    return disease_names[predicted_disease]

def show_attribute_descriptions():
    attribute_descriptions = {
        "MDVP:Fo(Hz)": "Average vocal fundamental frequency",
        "MDVP:Fhi(Hz)": "Maximum vocal fundamental frequency",
        "MDVP:Flo(Hz)": "Minimum vocal fundamental frequency",
        "MDVP:Jitter(%)": "Several measures of variation in fundamental frequency",
        "MDVP:Jitter(Abs)": "Several measures of variation in fundamental frequency",
        "MDVP:RAP": "Several measures of variation in fundamental frequency",
        "MDVP:PPQ": "Several measures of variation in fundamental frequency",
        "Jitter:DDP": "Several measures of variation in fundamental frequency",
        "MDVP:Shimmer": "Several measures of variation in amplitude",
        "MDVP:Shimmer(dB)": "Several measures of variation in amplitude",
        "Shimmer:APQ3": "Several measures of variation in amplitude",
        "Shimmer:APQ5": "Several measures of variation in amplitude",
        "MDVP:APQ": "Several measures of variation in amplitude",
        "Shimmer:DDA": "Several measures of variation in amplitude",
        "NHR": "Two measures of ratio of noise to tonal components in the voice",
        "HNR": "Two measures of ratio of noise to tonal components in the voice",
        "status": "Health status of the subject (one) - Parkinson's, (zero) - healthy",
        "RPDE": "Two nonlinear dynamical complexity measures",
        "D2": "Two nonlinear dynamical complexity measures",
        "DFA": "Signal fractal scaling exponent",
        "spread1": "Three nonlinear measures of fundamental frequency variation",
        "spread2": "Three nonlinear measures of fundamental frequency variation",
        "PPE": "Three nonlinear measures of fundamental frequency variation",
    }

    st.header("Attribute Descriptions")
    for attribute, description in attribute_descriptions.items():
        st.write(f"**{attribute}**: {description}")

def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
    return bmi

def interpret_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal Weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# sidebar for navigation
def main():
    with st.sidebar:
        image = Image.open('images/navbar.png')
        st.image(image, width=200)
        selected = option_menu('Disease Diagnosis and Recommendation System',
                               ['GENERAL', 'Diabetes Prediction',
                                'Heart Disease Prediction',
                                'Parkinsons Prediction', 'BMI CALCULATOR'],
                               icons=['dashboard', 'activity', 'heart', 'person', 'line-chart'],
                               default_index=0)

    if selected == 'GENERAL':
        st.title("General Diagnosis")
        st.write("Please enter the following information:")
        col1, col2 = st.columns([2, 1])
        with col1:
            # Get user input
            temp_f = st.text_input("Temperature (F):", value=0)
            pulse_rate_bpm = st.text_input("Pulse rate (bpm):", value=0)
            st.write("Check the Symptoms you have below:")
            vomiting = st.checkbox("Vomiting")
            yellowish_urine = st.checkbox("Yellowish Urine")
            indigestion = st.checkbox("Indigestion")

            # Predict disease based on user input
            if st.button("Test Result"):
                predicted_disease = predict_disease(temp_f, pulse_rate_bpm, vomiting, yellowish_urine, indigestion)
                medicine_recommendations = {
                    'Heart Disease': 'Follow a heart-healthy diet and exercise regularly.\nIt is crucial to attend all scheduled appointments with your doctor for proper monitoring and management.',
                    'Viral Fever/Cold': 'Get plenty of rest and stay hydrated.\nIf your fever persists or is accompanied by severe symptoms, visit a doctor for proper evaluation and treatment.',
                    'Jaundice': 'Rest, stay well-hydrated, and follow a balanced diet.\nIf you notice yellowing of the skin or eyes (jaundice), seek medical attention immediately for proper diagnosis and treatment.',
                    'Food Poisoning': 'Stay hydrated and avoid solid foods until symptoms subside.\nIf you experience severe symptoms, seek medical attention promptly for proper evaluation and treatment.',
                    'Normal': 'Maintain a healthy lifestyle with regular exercise and a balanced diet.\nEven if you are feeling well, have regular check-ups with your doctor to monitor your overall health.'
                }

                # Show the pop-up box with disease prediction and medicine recommendation
                if predicted_disease in medicine_recommendations:
                    medicine_recommendation = medicine_recommendations[predicted_disease]
                    st.info(f"Predicted Disease: {predicted_disease}")
                    with st.expander("Medicine Recommendation:"):
                        st.info(f"Medicine Recommendation: {medicine_recommendation}")
                else:
                    st.warning("Unknown disease prediction. Please check your input and try again.")

        with col2:
            image = Image.open('images/general.png')
            st.image(image, width=500)

    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        # page title
        st.title('Diabetes Prediction')

        # getting the input data from the user
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            Pregnancies = st.text_input('No of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age')

        with col4:
            image = Image.open('images/diabetes.png')
            st.image(image, width=400)

        # code for Prediction
        diab_diagnosis = ''

        # creating a button for Prediction

        if st.button('Diabetes Test Result'):
            diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

            if diab_prediction[0] == 1:
                st.success('The person is diabetic')
                with st.expander("Medicine Recommendation:"):
                    st.info(f"Medicine Recommendation: {'Please Consult a Medical Professional. Follow a balanced and healthy diet. It is important to exercise regularly.'}")
            else:
                st.success('The person is not diabetic')

    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        # page title
        st.title('Heart Disease Prediction')

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            age = st.text_input('Age')

        with col2:
            sex_options = ['Male', 'Female']
            sex = st.selectbox('Sex', sex_options)

        with col3:
            cp = st.text_input('Chest Pain type')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholesterol')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic Results')

        with col2:
            thalach = st.text_input('Maximum Heart Rate')

        with col3:
            exang = st.text_input('Exercise Induced Angina')

        with col1:
            oldpeak = st.text_input('Oldpeak')

        with col2:
            slope = st.text_input('Slope of the Peak Exercise ST Segment')

        with col3:
            ca = st.text_input('Number of Major Vessels colored by Flourosopy')

        with col1:
            thal = st.text_input('Thalassemia')

        with col4:
            image = Image.open('images/heart.png')
            st.image(image, width=400)

        # Heart Disease Prediction Code
        heart_diagnosis = ''

        if st.button('Heart Disease Test Result'):
            heart_prediction = heart_disease_model.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

            if heart_prediction[0] == 1:
                st.success('The person is suffering from heart disease')
                with st.expander("Medicine Recommendation:"):
                    st.info(f"Medicine Recommendation: {'Please consult a cardiologist for proper treatment. Keep track of blood pressure and cholesterol.'}")
            else:
                st.success('The person is not suffering from heart disease')

    # Parkinsons Prediction Page
    if selected == 'Parkinsons Prediction':
        # Page Title
        st.title("Parkinson's Disease Prediction")
        show_attribute_descriptions()

        # Getting Input from User
        col1, col2 = st.columns(2)

        with col1:
            MDVP_Fo = st.text_input("MDVP:Fo(Hz)")

        with col2:
            MDVP_Fhi = st.text_input("MDVP:Fhi(Hz)")

        # Prediction Button
        if st.button("Test Result"):
            parkinsons_prediction = parkinsons_model.predict([[MDVP_Fo, MDVP_Fhi]])

            if parkinsons_prediction[0] == 1:
                st.success('The person is likely suffering from Parkinson\'s Disease')
            else:
                st.success('The person is healthy')

    if selected == "BMI CALCULATOR":
        # BMI Page Title
        st.title('BMI Calculator')

        weight = st.number_input('Weight (kg)', min_value=0.0, step=0.1)
        height = st.number_input('Height (cm)', min_value=0.0, step=0.1)

        if st.button('Calculate BMI'):
            bmi = calculate_bmi(weight, height)
            st.write(f"BMI: {bmi:.2f}")
            st.write(f"Interpretation: {interpret_bmi(bmi)}")

    st.markdown("""
        <footer>
            Created by &copy; HelvinMG
        </footer>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == '__main__':
    main()
