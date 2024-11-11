import streamlit as st
import pandas as pd
import openai
import time
from datetime import timedelta
import os

# Set your OpenAI API key
openai.api_key = "OPEN_API_KEY"  # Replace with your actual API key

# Define city and state map with file paths relative to the repository's root directory
city_state_map = {
    "Los Angeles, CA": "openmeteoLA.csv",
    "San Jose, CA": "openmeteoSJ.csv",
    "New Orleans, LA": "openmeteoNewOrleans.csv",
    "Fort Lauderdale, FL": "openmeteoFortL.csv",
    "New York, NY": "openmeteoNY.csv"
}

# Load the CSV file based on city selection
def load_data(city_file):
    file_path = os.path.join("data", city_file)  # Using a relative path to the 'data' directory
    try:
        df = pd.read_csv(file_path)
        df.columns = df.columns.str.strip()  # Remove any extra whitespace from column names
        
        if 'time' in df.columns:
            df["time"] = pd.to_datetime(df["time"], errors='coerce')
            return df, "time"
        else:
            st.error(f"The 'time' column was not found in the file: {city_file}.")
            return None, None
    except FileNotFoundError:
        st.error(f"The file {city_file} could not be found in the 'data' directory. Please check the file path.")
        return None, None
    except Exception as e:
        st.error(f"An error occurred while loading the data for {city_file}: {e}")
        return None, None

# Calculate water saved by skipping watering on rainy days
def calculate_water_savings(df, daily_watering_gallons=5):
    rainy_days = df[df['precipitation'] > 0]
    water_saved = len(rainy_days) * daily_watering_gallons  # Water saved in gallons
    return water_saved

# Calculate water-to-tree equivalent
def calculate_tree_impact(water_saved_gallons, water_per_tree_gallons=20):
    trees = water_saved_gallons / water_per_tree_gallons
    return int(trees)

# Generate recommendations using OpenAI ChatCompletion API with retry for rate limit error
def generate_recommendations(prediction_df, water_saved, trees_plantable):
    prediction_summary = prediction_df.to_string(index=False)
    impact_statement = (
        f"By skipping watering on rainy days, you saved approximately {water_saved} gallons of water, "
        f"which could support the planting of {trees_plantable} trees."
    )

    prompt = (
        f"Based on the following future weather predictions:\n{prediction_summary}\n\n"
        f"{impact_statement}\n\n"
        "Provide recommendations for household water conservation and usage strategies that would have a bigger impact."
    )
    
    max_retries = 5  # Set the number of retries
    retry_delay = 20  # Time to wait (in seconds) between retries if rate limit is hit

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an assistant providing water conservation tips based on weather data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.5
            )
            return impact_statement + "\n\n" + response['choices'][0]['message']['content'].strip()
        
        except openai.error.RateLimitError as e:
            if attempt < max_retries - 1:
                st.warning(f"Rate limit reached. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)  # Wait before retrying
            else:
                st.error("Rate limit exceeded. Please try again later.")
                return "Rate limit exceeded. Please try again later."

# Streamlit app
def main():
    st.title("Enhanced Weather Data Analysis with Predictions and Recommendations")

    # User selection for city and state
    city_state = st.selectbox("Choose a city:", list(city_state_map.keys()))
    city_file = city_state_map[city_state]  # Get the corresponding file name
    
    # Load and process data based on the selected city
    df, date_column = load_data(city_file)
    
    if df is not None and date_column:
        # Calculate water savings by skipping watering on rainy days
        water_saved = calculate_water_savings(df)
        
        # Calculate how many trees could be planted with the saved water
        trees_plantable = calculate_tree_impact(water_saved)
        
        # Display daily precipitation chart
        st.subheader("Daily Precipitation (inches)")
        st.line_chart(df.set_index('time')['precipitation'])
        
        # Monthly data aggregation
        monthly_data = df.resample('M', on='time').agg({
            'temperature': 'mean',
            'precipitation': 'sum'
        }).reset_index()
        st.subheader(f"Monthly Weather Data for {city_state}")
        st.write(monthly_data)
        
        # Plot monthly temperature
        st.subheader("Average Monthly Temperature (°F)")
        st.line_chart(monthly_data.set_index('time')['temperature'])
        
        # Future pattern prediction
        st.subheader("Predicted Future Weather Patterns")
        future_df = pd.DataFrame({
            'date': [df['time'].max() + timedelta(days=i*30) for i in range(1, 4)],
            'predicted_temperature': [monthly_data['temperature'].mean()] * 3,
            'predicted_precipitation': [monthly_data['precipitation'].mean()] * 3
        })
        st.write(future_df)
        
        # Water Savings and Tree Planting Potential chart
        st.subheader("Water Savings and Tree Planting Potential")
        
        water_data = pd.DataFrame({
            'Metric': ['Water Saved (Gallons)', 'Trees Plantable'],
            'Value': [water_saved, trees_plantable]
        })
        st.bar_chart(water_data.set_index('Metric'))
        
        # Generative AI recommendations with tree impact statement
        st.subheader("Recommendations for a Bigger Impact")
        recommendations = generate_recommendations(future_df, water_saved, trees_plantable)
        st.write(recommendations)
    else:
        st.error("Data for the selected city is not available or the date column was not found.")

if __name__ == "__main__":
    main()
