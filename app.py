import streamlit as st
import pandas as pd
import numpy as np
from real_model import predict_home_automation, load_models
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
The system will suggest appropriate brightness levels for each room's lighting.
""")

# Initialize model
if not initialize_model():
    st.error("Please check your model files and try again.")
    st.stop()

# Add tabs for different modes
tab1, tab2 = st.tabs(["Standard Mode", "Custom Testing Mode"])

with tab1:
    # Sidebar for input parameters
    st.header("Standard Input Parameters")

    # Create input fields
    col1, col2 = st.columns(2)

    with col1:
        mood = st.selectbox(
            "Mood",
            ["peaceful", "focused", "tired", "stressed", "happy", "calm", "energetic"],
            key="mood1"
        )
        
        person_condition = st.selectbox(
            "Current Condition",
            ["sleeping", "at_work", "at_home", "out", "getting_ready", "awake"],
            key="condition1"
        )
        
        time_of_day = st.selectbox(
            "Time of Day",
            ["morning", "afternoon", "evening", "night"],
            key="time1"
        )

    with col2:
        at_home = st.radio(
            "Are you at home?",
            ["Yes", "No"],
            key="home1"
        )
        
        is_holiday = st.radio(
            "Is it a holiday?",
            ["Yes", "No"],
            key="holiday1"
        )

    # Convert inputs to model format
    at_home_val = 1 if at_home == "Yes" else 0
    is_holiday_val = 1 if is_holiday == "Yes" else 0

    # Add a predict button
    if st.button("Get Recommendations", key="predict1"):
        try:
            # Get predictions
            recommendations = predict_home_automation(
                mood=mood,
                person_condition=person_condition,
                time_of_day=time_of_day,
                at_home=at_home_val,
                is_holiday=is_holiday_val
            )
            
            if recommendations:
                st.success("Here are your recommended actions:")
                for i, action in enumerate(recommendations, 1):
                    st.write(f"{i}. {action}")
            else:
                st.error("Failed to generate recommendations. Please try again.")
        except ValueError as e:
            st.error(f"Invalid input: {str(e)}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

with tab2:
    st.header("Custom Testing Mode")
    st.markdown("""
    In this mode, you can test the model with custom scenarios. 
    You can input multiple scenarios and see how the model responds to different combinations.
    """)

    # Create columns for custom inputs
    custom_col1, custom_col2 = st.columns(2)

    with custom_col1:
        # Custom mood input
        custom_mood = st.text_input(
            "Custom Mood",
            placeholder="Enter any mood (e.g., 'excited', 'relaxed')",
            help="The model will map unknown moods to the closest known mood"
        )

        # Custom condition input
        custom_condition = st.text_input(
            "Custom Condition",
            placeholder="Enter any condition (e.g., 'working', 'exercising')",
            help="The model will map unknown conditions to the closest known condition"
        )

        # Custom time input
        custom_time = st.text_input(
            "Custom Time of Day",
            placeholder="Enter any time description",
            help="The model will map unknown times to morning/afternoon/evening/night"
        )

    with custom_col2:
        custom_at_home = st.radio(
            "At Home Status",
            ["Yes", "No", "Custom"],
            key="home2"
        )
        
        if custom_at_home == "Custom":
            custom_at_home = st.text_input(
                "Custom At Home Status",
                placeholder="Enter any status"
            )

        custom_is_holiday = st.radio(
            "Holiday Status",
            ["Yes", "No", "Custom"],
            key="holiday2"
        )
        
        if custom_is_holiday == "Custom":
            custom_is_holiday = st.text_input(
                "Custom Holiday Status",
                placeholder="Enter any status"
            )

    # Add explanation for custom inputs
    st.info("""
    Note: When using custom inputs, the model will try to map your inputs to the closest matching known values.
    This helps test how the model handles unexpected or new situations.
    """)

    # Process custom inputs
    if st.button("Test Custom Scenario", key="predict2"):
        try:
            # Map custom inputs to known values
            mapped_mood = custom_mood if custom_mood in ["peaceful", "focused", "tired", "stressed", "happy", "calm", "energetic"] else "happy"
            mapped_condition = custom_condition if custom_condition in ["sleeping", "at_work", "at_home", "out", "getting_ready", "awake"] else "at_home"
            mapped_time = custom_time if custom_time in ["morning", "afternoon", "evening", "night"] else "afternoon"
            
            # Map at_home and is_holiday
            if custom_at_home == "Custom":
                mapped_at_home = 1  # Default to at home for custom values
            else:
                mapped_at_home = 1 if custom_at_home == "Yes" else 0
                
            if custom_is_holiday == "Custom":
                mapped_is_holiday = 0  # Default to not holiday for custom values
            else:
                mapped_is_holiday = 1 if custom_is_holiday == "Yes" else 0


            # Get predictions
            recommendations = predict_home_automation(
                mood=mapped_mood,
                person_condition=mapped_condition,
                time_of_day=mapped_time,
                at_home=mapped_at_home,
                is_holiday=mapped_is_holiday
            )
            
            if recommendations:
                st.success("Here are your recommended actions for the custom scenario:")
                for i, action in enumerate(recommendations, 1):
                    st.write(f"{i}. {action}")
            else:
                st.error("Failed to generate recommendations for custom scenario.")
        except Exception as e:
            st.error(f"An error occurred with custom inputs: {str(e)}")

# Add some additional information
st.markdown("""
---
### About the Model
This smart home automation system uses machine learning to predict optimal settings for:
- Device control (TV, music, security systems)
- Lighting control with smart brightness levels
- Music type recommendations

The model takes into account your:
- Current mood
- Activity/condition
- Time of day
- Location (at home/away)
- Holiday status

The lighting system will automatically adjust brightness based on:
- Time of day (brighter during day, dimmer at night)
- Your activity (bright for tasks, dim for relaxing)
- Your condition (very dim when sleeping, bright when getting ready)
""") 