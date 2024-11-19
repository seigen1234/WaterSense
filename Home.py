import streamlit as st
import os
from PIL import Image

# Set up page configuration
st.set_page_config(page_title="WaterSense", page_icon="💧", layout="wide")

# Path to the logo image (if needed)
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
        .stNumberInput, .stTextInput{
            border-radius: 10px;
            background-color: #d8eefe;
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

# Title and description of the app
st.title("WaterSense")
st.markdown("""
Welcome to the Water Conservation & Usage Application! This tool is designed to help you monitor and manage your household's water usage effectively. 
Through this app, you can track your water consumption, receive personalized conservation tips, and see potential savings based on your usage patterns.
""")

# Add the disclaimer button
if st.button('Disclaimer'):
    st.markdown("""
    ### DISCLAIMER

    When using this application, household information may be shared with third-party APIs to provide enhanced features and services. Please be aware that:
    
    - Third-party APIs may collect, process, and store the data you provide.
    - While we strive to utilize reputable services, we cannot fully control how third parties handle your information.
    - There is a potential risk of data misuse or unauthorized access by third parties.
    
    We strongly recommend that you:
    - Review the privacy policies of any third-party APIs utilized by this app.
    - Only share information you are comfortable disclosing.
    
    **By using this application, you acknowledge and accept these risks.**
    """)

# Dropdown for quick access to different app pages
page = st.selectbox(
    "Select a Page to Navigate:",
    ("Select a Page", "Water Usage Tracker", "Water Conservation Utility Guide", "Weather Data Analysis & Recommendations")
)

# Handle the page selection logic
if page == "Select a Page":
    # Just display the main page content without any page load
    st.write("Please select a page to navigate.")
elif page == "Water Usage Tracker":
    exec(open("pages/page_1.py").read())  # Function from page_1.py
elif page == "Water Conservation Utility Guide":
    exec(open("pages/page_2.py").read())  # Load page_2.py dynamically
elif page == "Weather Data Analysis & Recommendations":
    exec(open("pages/page_3.py").read())  # Load page_3.py dynamically



import streamlit as st

# CSS for transparent sidebar background and logo positioning
custom_css = """
<style>
    /* Make sidebar background transparent */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.8); /* Adjust transparency */
    }
    /* Center and adjust logo in the sidebar */
    [data-testid="stSidebar"] img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        margin-bottom: 20px;
    }
</style>
"""

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Path to your logo file
logo_path = "logo.png"  # Replace with the correct path to your logo

# Display the logo at the top of the sidebar
with st.sidebar:
    st.image(logo_path, use_column_width=True)  # Add logo above the navigation tabs

# Example main content
st.title("Welcome to WaterSense!")
st.write("This is your app content.")
