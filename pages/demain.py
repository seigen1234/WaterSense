import streamlit as st
import pages.page_3 as weather
import pages.page_1 as water_meter
import pages.page_2 as water_calculator

# Main page with navigation
st.title("Water Conservation App")

# Sidebar navigation for different features
feature_choice = st.sidebar.radio("Choose a Feature:", 
                                  ("Weather Analysis", "Water Meter Tracker", "Water Usage Calculator"))

# Display the selected feature
if feature_choice == "Weather Analysis":
    page_3.main()  # Calls the main function in weather.py
elif feature_choice == "Water Meter Tracker":
    page_1.main()  # Calls the main function in WaterMeterCalculatorAPI.py
elif feature_choice == "Water Usage Calculator":
    page_2.main()  # Calls the main function in watercalc2.py
