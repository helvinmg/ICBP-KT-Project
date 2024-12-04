import streamlit as st

# Adding custom CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }

    /* Header customization */
    .custom-header {
        font-size: 30px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Highlighted text */
    .highlight {
        color: #ff5722;
        font-weight: bold;
    }

    /* Styled button */
    .stButton>button {
        background-color: #6200ea;
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #3700b3;
    }

    /* Text input customization */
    input[type="text"] {
        border: 2px solid #4CAF50;
        padding: 5px;
        border-radius: 5px;
    }

    /* File uploader */
    .stFileUploader {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 10px;
        border: 2px dashed #1e88e5;
    }
    </style>
""", unsafe_allow_html=True)

st.success("success")
st.error("error")
# Header with custom styles
st.markdown('<div class="custom-header">Styled Form by Helvin</div>', unsafe_allow_html=True)

# Checkbox with dynamic response
if st.checkbox('Agree to the terms and conditions?'):
    st.markdown('<p class="highlight">Thank you for agreeing!</p>', unsafe_allow_html=True)

# Button with applied styles
if st.button('Submit Form'):
    st.markdown('<p class="highlight">Form Submitted Successfully!</p>', unsafe_allow_html=True)

# Radio buttons
gender = st.radio('Select your gender', ['Male', 'Female', 'Other'])
st.write(f"You selected: **{gender}**")

# Selectbox
fruit = st.selectbox('Pick your favorite fruit', ['Apple', 'Banana', 'Orange', 'Mango'], index=2)
st.write(f"You selected: **{fruit}**")

# Multiselect
planets = st.multiselect('Choose the planets you like', 
                         ['Jupiter', 'Mars', 'Neptune', 'Earth', 'Venus'], 
                         default=['Earth', 'Mars'])
st.write(f"You selected: {', '.join(planets)}")

# Slider
number = st.slider('Pick a number', 0, 100, 50, step=5)
st.write(f"You picked: **{number}**")

# Number input
num_input = st.number_input('Pick a number between 1 and 10', 1, 10, 5)
st.write(f"Your number: **{num_input}**")

# Text input with placeholder
email = st.text_input('Enter your email address', placeholder='example@domain.com')
st.write(f"Your email: **{email}**")

# Date input
travel_date = st.date_input('Select your travel date')
st.write(f"Your travel date: **{travel_date}**")

# Time input
office_time = st.time_input('Set your office hours')
st.write(f"Office hours start at: **{office_time}**")

# Text area
description = st.text_area('Provide a description', height=150)
st.write(f"Your description: **{description}**")

# File uploader with styled container
uploaded_file = st.file_uploader('Upload a photo or document', type=['jpg', 'png', 'pdf'])
if uploaded_file:
    st.write(f"Uploaded file: **{uploaded_file.name}**")

# Color picker
color = st.color_picker('Choose your favorite color', value='#00f900')
st.write(f"Your selected color is: **{color}**")
