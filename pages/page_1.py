import streamlit as st
import pandas as pd
import requests
import openai
import os  # Import the os module
from datetime import datetime, timedelta

# UtilityAPI base URL and headers (replace 'YOUR_API_KEY' with actual API key)
API_URL = 'https://utilityapi.com/api/v2/meters/{meter_id}/intervals'
headers = {'Authorization': 'Bearer YOUR_API_KEY'}

# OpenAI API setup (ensure your OpenAI API key is set as an environment variable)
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    st.error("OpenAI API key is missing. Please set the 'OPENAI_API_KEY' environment variable.")
else:
    openai.api_key = openai_api_key

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

# Function to provide suggestions based on efficiency score
def get_suggestions(efficiency_score):
    if efficiency_score < -50:  # Significantly inefficient usage
        return [
            "Your water usage is much higher than expected. Try taking shorter showers, fixing leaks, and using water-saving appliances.",
            "Consider using a broom instead of a hose to clean driveways and sidewalks.",
            "Check your irrigation system regularly for leaks or inefficient settings.",
            "You may benefit from installing low-flow fixtures or even a smart irrigation controller."
        ]
    elif -50 <= efficiency_score < -20:  # Moderately inefficient usage
        return [
            "Your water usage is higher than expected. Try to reduce shower times and avoid letting water run unnecessarily.",
            "Consider watering plants early in the morning or late evening to minimize evaporation.",
            "Check your home for any minor leaks or areas where you can conserve more."
        ]
    elif -20 <= efficiency_score < 0:  # Slightly inefficient usage
        return [
            "You're close to the expected usage. Reducing water usage slightly could help you improve your efficiency score.",
            "Try small changes, like turning off the tap while brushing your teeth or washing dishes more efficiently.",
            "Consider reusing water where possible, like capturing rainwater for outdoor plants."
        ]
    elif 0 <= efficiency_score < 20:  # Efficient usage
        return [
            "Great job! You're using water close to the expected amount. Keep up these habits!",
            "Consider sharing your conservation practices with friends or family to encourage efficient water use.",
            "Think about further steps like installing rainwater harvesting systems or smart water sensors."
        ]
    elif 20 <= efficiency_score < 50:  # Highly efficient usage
        return [
            "Excellent job! Your water usage is below expected levels, which means you're conserving well.",
            "Maintain these habits to continue conserving water effectively.",
            "Consider periodic checks of appliances and fixtures to ensure ongoing efficiency."
        ]
    else:  # Extremely efficient usage
        return [
            "Outstanding! Your water usage is well below expected levels.",
            "Keep up the great habits, and consider sharing your tips with others.",
            "Stay mindful of any sudden changes, and keep up with regular maintenance for sustained efficiency."
        ]
    
def get_chatbot_response(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message['content']

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
        st.metric(label="Efficiency Score (Average is 0%)", value=f"{efficiency_score:.2f}%")

        # Efficiency explanation
        st.markdown("""
        ### Understanding Your Efficiency Score:
        - **Efficiency Score**: Measures your water usage against an average expected usage based on the number of people in your household.
        - **Score Calculation Formula**:
          - Average Expected Usage: `Number of People × 50 gallons/day × 7 days`
          - Efficiency Score: `100 - (Total Usage / Average Expected Usage × 100)`
        """)

        # Provide suggestions based on efficiency score
        st.markdown("### 💡 Suggestions to Improve Efficiency")
        suggestions = get_suggestions(efficiency_score)
        for suggestion in suggestions:
            st.write(f"- {suggestion}")

    # Add Chatbot Feature
    st.markdown("### 🤖 Ask the Water Habits Chatbot")
    user_input = st.text_input("What would you like to know about water habits?")

    if st.button("Ask"):
        if user_input:
            response = get_chatbot_response(user_input)
            st.write("**Chatbot Response:**")
            st.write(response)
        else:
            st.write("Please enter a question to ask the chatbot.")

# Running the app
if __name__ == "__main__":
    water_usage_tracker()

