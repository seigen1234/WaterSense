import streamlit as st

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
        import page_1  # Import the page 1 code here

elif app_selection == "Water Conservation Guide":
    st.write("""
    **Water Conservation Guide**  
    Estimate your household's water consumption across various activities and discover effective strategies to save water and reduce your bill.
    """)
    if st.button("Go to Water Conservation Guide"):
        import page_2  # Import the page 2 code here

elif app_selection == "Weather & Water Analysis":
    st.write("""
    **Weather & Water Analysis**  
    Use weather data to understand the best times to conserve water, track precipitation trends, and get eco-friendly recommendations to maximize water efficiency.
    """)
    if st.button("Go to Weather & Water Analysis"):
        import page_3  # Import the page 3 code here
