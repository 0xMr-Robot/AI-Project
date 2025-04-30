import streamlit as st
import pandas as pd
import numpy as np
from real_model import predict_home_automation, validate_input, load_models
import datetime

# Initialize the model
@st.cache_resource
def initialize_model():
    if load_models():
        st.success("Model loaded successfully!")
        return True
    else:
        st.error("Failed to load model!")
        return False

# Set page config
st.set_page_config(
    page_title="Smart Home Automation",
    page_icon="🏠",
    layout="wide"
)

# Title and description
st.title("🏠 Smart Home Automation System")
st.markdown("""
This application predicts optimal home automation settings based on your current state and preferences.
""")

# Initialize model
if not initialize_model():
    st.error("Please check your model files and try again.")
    st.stop()

# Sidebar for input parameters
st.sidebar.header("Input Parameters")

# Create input fields
col1, col2 = st.columns(2)

with col1:
    mood = st.selectbox(
        "Mood",
        ["peaceful", "focused", "tired", "stressed", "happy", "calm", "energetic"]
    )
    
    person_condition = st.selectbox(
        "Current Condition",
        ["sleeping", "at_work", "at_home", "out", "getting_ready", "awake"]
    )
    
    time_of_day = st.selectbox(
        "Time of Day",
        ["morning", "afternoon", "evening", "night"]
    )

with col2:
    at_home = st.radio(
        "Are you at home?",
        ["Yes", "No"]
    )
    
    is_holiday = st.radio(
        "Is it a holiday?",
        ["Yes", "No"]
    )
    
    current_time = st.time_input("Current Time")
    current_date = st.date_input("Current Date")

# Convert inputs to model format
at_home = 1 if at_home == "Yes" else 0
is_holiday = 1 if is_holiday == "Yes" else 0

# Add a predict button
if st.button("Get Recommendations"):
    # Validate inputs
    if validate_input(
        current_time=datetime.datetime.combine(current_date, current_time),
        current_date=current_date,
        person_condition=person_condition,
        at_home=at_home,
        is_holiday=is_holiday,
        guests_present=0,  # Default value
        mood=mood,
        temperature=22,    # Default value
        light_level=500    # Default value
    ):
        # Get predictions
        recommendations = predict_home_automation(
            mood=mood,
            person_condition=person_condition,
            time_of_day=time_of_day,
            at_home=at_home,
            is_holiday=is_holiday
        )
        
        if recommendations:
            st.success("Here are your recommended actions:")
            for i, action in enumerate(recommendations, 1):
                st.write(f"{i}. {action}")
        else:
            st.error("Failed to generate recommendations. Please try again.")
    else:
        st.error("Invalid input parameters. Please check your inputs.")

# Add some additional information
st.markdown("""
---
### About the Model
This smart home automation system uses machine learning to predict optimal settings for:
- Device control (TV, music, security systems)
- Lighting control (bedroom, living room, bathroom, kitchen)
- Music type recommendations

The model takes into account your current mood, condition, time of day, and whether you're at home or it's a holiday.
""") 