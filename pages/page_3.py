import streamlit as st
import pandas as pd
from datetime import datetime
import openai

# Set your OpenAI API key
openai.api_key = "OPENAI_API_KEY"  # Replace with your actual API key

# Mapping of city names to file paths
city_files = {
    "San Francisco": "data/SanFrancisco.csv",
    "San Jose": "data/SanJose.csv",
    "Palo Alto": "data/Palo Alto.csv",
    "Berkeley": "data/Berkeley.csv",
    "Fremont": "data/Fremont.csv"
}

# Function to load data based on the selected city
def load_city_data(city):
    """Load the CSV file for the selected city."""
    file_path = city_files.get(city)
    if file_path:
        try:
            data = pd.read_csv(file_path)
            # Ensure time column is in datetime format
            data['time'] = pd.to_datetime(data['time'])
            return data
        except Exception as e:
            st.error(f"Error loading data for {city}: {e}")
    return None

# Determine current season based on month
def get_current_season():
    """Determine the current season based on the month."""
    month = datetime.now().month
    return "Rainy" if month in [11, 12, 1, 2, 3, 4] else "Drought"

# Display summary of average temperature and precipitation
def display_data_summary(data):
    """Display average temperature and precipitation by month."""
    if data is not None:
        if "time" in data.columns and "temperature" in data.columns and "precipitation" in data.columns:
            data['month'] = data['time'].dt.month
            monthly_summary = (
                data.groupby("month")[["temperature", "precipitation"]]
                .mean()
                .rename(columns={"temperature": "Avg Temperature (°F)", "precipitation": "Avg Precipitation (in)"})
            )
            monthly_summary.index = monthly_summary.index.map(lambda x: datetime(1900, x, 1).strftime("%B"))
            st.write("### Monthly Averages")
            st.dataframe(monthly_summary)
        else:
            st.warning("Required data columns (time, temperature, precipitation) are not available.")
    else:
        st.warning("No data available for the selected city.")

# Generate fun facts and insights
def generate_fun_facts_and_insights(data, city):
    """Generate fun facts about rainwater collection and creative insights."""
    if data is None or 'precipitation' not in data.columns:
        st.warning("Precipitation data is unavailable for insights.")
        return None

    # Data analysis: Rainwater collection
    roof_size = 1000  # Assume 1,000 square feet of roof
    gallon_per_inch_per_sqft = 0.623  # Gallons collected per inch of rain per square foot
    total_precip = data['precipitation'].sum()  # Total precipitation in inches
    rainwater_collected = roof_size * total_precip * gallon_per_inch_per_sqft

    # Fun facts
    fun_facts = [
        f"With {total_precip:.2f} inches of rain this season, a 1,000 square-foot roof could collect approximately {rainwater_collected:.0f} gallons of water.",
        f"This amount of water could fill approximately {rainwater_collected / 80:.0f} standard bathtubs!",
        f"Alternatively, this water could hydrate {rainwater_collected / 5:.0f} medium-sized trees for a month.",
        f"Or, it could supply drinking water for one person for {rainwater_collected / 13.2:.0f} days, based on average daily usage."
    ]

    # Display fun facts
    st.write("### Fun Facts About Rainwater Collection")
    for fact in fun_facts:
        st.write(f"- {fact}")

    # Generate creative AI insights using OpenAI
    prompt = (
        f"The city of {city} has received {total_precip:.2f} inches of rain this season, which could collect approximately {rainwater_collected:.0f} gallons of water. "
        "Generate creative and impactful suggestions for using this rainwater to benefit the community and support environmental sustainability. "
        "Focus on innovative, community-centered, and social good applications."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant focused on sustainability and social good."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.7
        )
        insights = response.choices[0].message["content"].strip()
        st.write("### AI-Powered Insights")
        st.write(insights)
    except Exception as e:
        st.error(f"Error generating AI insights: {e}")

# Streamlit UI
st.title("Bay Area Weather & Water Conservation Insights")
st.subheader("Get localized weather data, actionable water-saving tips, and impactful AI-driven insights!")

# City selection
cities = list(city_files.keys())
selected_city = st.selectbox("Select a city:", cities)

# Load data based on the selected city
data = load_city_data(selected_city)

# Display data summary
if data is not None:
    display_data_summary(data)

# Generate fun facts and insights
if st.button("Generate Fun Facts and AI-Powered Insights"):
    current_season = get_current_season()
    st.write(f"### Current Season: {current_season}")
    generate_fun_facts_and_insights(data, selected_city)
