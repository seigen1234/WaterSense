import streamlit as st
import importlib

# App title and description
st.title("EcoFlow Insights")
st.write("""
Welcome to EcoFlow Insights, a suite of tools designed to help you monitor, optimize, and conserve water usage. 
Choose an application below to start making a difference in your water habits!
""")

# Dropdown for application selection
app_selection = st.selectbox("Select an Application", ["Water Usage Tracker", "Water Conservation Guide", "Weather & Water Analysis"])

# Display brief descriptions and links to each app
if app_selection == "Water Usage Tracker":
    st.write("""
    **Water Usage Tracker**  
    Track and analyze your water usage patterns, estimate efficiency scores, and receive personalized water-saving suggestions based on your household usage.
    """)
    if st.button("Go to Water Usage Tracker"):
        # Dynamically load or reload page_1
        page_1 = importlib.import_module("pages.page_1")
        importlib.reload(page_1)
        page_1.run()  # Ensure `run()` or similar function is defined in page_1.py to display the content

elif app_selection == "Water Conservation Guide":
    st.write("""
    **Water Conservation Guide**  
    Estimate your household's water consumption across various activities and discover effective strategies to save water and reduce your bill.
    """)
    if st.button("Go to Water Conservation Guide"):
        # Dynamically load or reload page_2
        page_2 = importlib.import_module("pages.page_2")
        importlib.reload(page_2)
        page_2.run()  # Ensure `run()` or similar function is defined in page_2.py to display the content

elif app_selection == "Weather & Water Analysis":
    st.write("""
    **Weather & Water Analysis**  
    Use weather data to understand the best times to conserve water, track precipitation trends, and get eco-friendly recommendations to maximize water efficiency.
    """)
    if st.button("Go to Weather & Water Analysis"):
        # Dynamically load or reload page_3
        page_3 = importlib.import_module("pages.page_3")
        importlib.reload(page_3)
        page_3.run()  # Ensure `run()` or similar function is defined in page_3.py to display the content
