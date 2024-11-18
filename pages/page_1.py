import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# UtilityAPI base URL and headers (replace 'YOUR_API_KEY' with actual API key)
API_URL = 'https://utilityapi.com/api/v2/meters/{meter_id}/intervals'
headers = {'Authorization': 'Bearer YOUR_API_KEY'}


def load_interval_data_csv(file_path):
    return pd.read_csv(file_path)


def load_interval_data_api(meter_id, start_date, end_date):
    url = API_URL.format(meter_id=meter_id)
    params = {'start': start_date, 'end': end_date}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return pd.DataFrame(response.json()['intervals'])
    else:
        st.error("Failed to fetch data from UtilityAPI.")
        return pd.DataFrame()


def water_usage_tracker():
    # Main content for Water Usage Tracker
    st.markdown("### 🌊 Welcome to the Water Usage Tracker!")
    st.write("This tool is designed to help you monitor and manage your household's water usage efficiently.")

    st.markdown("#### 📂 Select a Data Source")
    data_source = st.selectbox("Choose an option:", ("Water Usage Data", "Meter ID input (Real Time Water Usage)"))
    interval_data = pd.DataFrame()

    if data_source == "Water Usage Data":
        # Load data from a predefined CSV file
        file_path = 'pages/synthetic_water_usage_data.csv'
        interval_data = load_interval_data_csv(file_path)
    else:
        # Fetch real-time data using UtilityAPI
        meter_id = st.text_input("Enter Meter ID for UtilityAPI")
        if meter_id:
            selected_date = st.date_input("Select a date within the week", datetime.now())
            start_of_week = (selected_date - timedelta(days=selected_date.weekday())).strftime('%Y-%m-%d')
            end_of_week = (datetime.strptime(start_of_week, '%Y-%m-%d') + timedelta(days=6)).strftime('%Y-%m-%d')
            interval_data = load_interval_data_api(meter_id, start_of_week, end_of_week)

    # Display and analyze data
    if not interval_data.empty:
        interval_data['start'] = pd.to_datetime(interval_data['start'])
        interval_data['week'] = interval_data['start'].dt.to_period('W')

        st.markdown("#### 📅 Select a Week to View Water Usage")
        week_options = interval_data['week'].unique()
        selected_week = st.selectbox("Choose a week:", week_options)

        # Filter data for the selected week
        weekly_data = interval_data[interval_data['week'] == selected_week]

        st.markdown(f"#### Water Usage Data for Week: {selected_week}")
        st.dataframe(weekly_data[['start', 'kwh']], use_container_width=True)

        # Calculate total usage and efficiency score
        total_usage_week = weekly_data['kwh'].sum()
        number_of_people = st.number_input("Enter the number of people in your household:", min_value=1, value=1)
        average_daily_usage = 50 * number_of_people  # 50 gallons per person per day
        average_usage = average_daily_usage * 7
        efficiency_score = 100 - ((total_usage_week / average_usage) * 100)

        # Display metrics
        st.metric(label="Total Usage for the Week", value=f"{total_usage_week:.2f} gallons")
        st.metric(label="Efficiency Score", value=f"{efficiency_score:.2f}%")

        # Efficiency explanation
        st.markdown("""
        ### Understanding Your Efficiency Score:
        - **Efficiency Score**: Measures your water usage against an average expected usage based on the number of people in your household.
        - **Score Calculation Formula**:
          - Average Expected Usage: `Number of People × 50 gallons/day × 7 days`
          - Efficiency Score: `100 - (Total Usage / Average Expected Usage × 100)`
        """)

    # Add Chatbot Feature
    st.markdown("### 🤖 Ask the Water Habits Chatbot")
    user_input = st.text_input("What would you like to know about water habits?")
    if st.button("Ask"):
        if user_input:
            st.write("Chatbot Response:")
            # Call OpenAI API here if functional
            st.write("This is where the chatbot response would appear.")
        else:
            st.warning("Please enter a question to ask the chatbot.")


# If the script is run independently
if "water_usage_tracker" not in st.session_state:
    water_usage_tracker()
