import streamlit as st
# Main page for Water Conservation Application
st.title("Water Conservation & Usage Application")
st.markdown("""
Welcome to the Water Conservation & Usage Application! This tool is designed to help you monitor and manage your household's water usage effectively. 
Through this app, you can track your water consumption, receive personalized conservation tips, and see potential savings based on your usage patterns.
""")

# Dropdown for quick access to different app pages
page = st.selectbox(
    "Select a Page to Navigate:",
    ("Water Usage Tracker", "Water Conservation Utility Guide", "Weather Data Analysis & Recommendations")
)

# Load the corresponding pages based on the dropdown selection
if page == "Water Usage Tracker":
    exec(open("pages/page_1.py").read())
elif page == "Water Conservation Utility Guide":
    exec(open("pages/page_2.py").read())
elif page == "Weather Data Analysis & Recommendations":
    exec(open("pages/page_3.py").read())
