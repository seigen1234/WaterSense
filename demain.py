import streamlit as st
import os
from PIL import Image
from pages.page_1 import water_usage_tracker
# Main page for Water Conservation Application


st.set_page_config(page_title="WaterSense", page_icon="💧", layout="wide")

# Path to the logo image
logo_path = os.path.join(os.getcwd(), "logo.png")




# Custom CSS styling
st.markdown(
    """
    <style>
        /* Background color */
        .main {
            background-color: #CAF0F8;
        }
        
        /* Sidebar styling */
        .css-1d391kg, .css-qbe2hs {
            background-color: #d8eefe;
            color: #005b5b;
        }
        
        /* Input and button styling */
        .stNumberInput, .stTextInput, .stButton {
            border-radius: 10px;
            background-color: #ffffff;
            border: 1px solid #87ceeb;
            padding: 8px;
            font-size: 16px;
        }

        /* Metric styling */
        .stMetric {
            font-size: 24px;
            color: #005b5b;
        }
        
        /* Headers styling */
        h1, h2, h3, h4 {
            color: #005b5b;
            font-family: 'Arial', sans-serif;
        }

        /* Text styling */
        .stMarkdown {
            font-size: 18px;
            line-height: 1.6;
        }

        /* Progress bar styling */
        .stProgress > div > div {
            background-color: #87ceeb;
        }
        
        /* Button styling */
        div.stButton > button {
            color: white;
            background-color: #005b5b;
            border: none;
            border-radius: 8px;
            padding: 8px 16px;
            font-size: 16px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }

        /* Button hover effect */
        div.stButton > button:hover {
            background-color: #007b7b;
        }

        /* Link styling */
        a {
            color: #005b5b;
            font-weight: bold;
        }

        /* Tooltip styling */
        .stTooltip {
            background-color: #87ceeb;
            color: #ffffff;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Your existing code here, without modification
st.title("WaterSense")
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
    water_usage_tracker()
elif page == "Water Conservation Utility Guide":
    exec(open("pages/page_2.py").read())
elif page == "Weather Data Analysis & Recommendations":
    exec(open("pages/page_3.py").read())
