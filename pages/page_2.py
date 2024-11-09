import os
import streamlit as st
import openai  # Import OpenAI library for generating advice

# Access the API key from environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")  # Ensure the API key is set in your environment as "OPENAI_API_KEY"
if openai_api_key is None:
    st.error("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
else:
    openai.api_key = openai_api_key

def generate_water_saving_advice(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=999
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key is None:
        st.error("OpenAI API key is not set. Please set the environment variable OPENAI_API_KEY.")
    else:
        openai.api_key = openai_api_key

    # Centered Logo and Title with EBMUD Link
    st.markdown(
        """
        <div style='text-align: center;'>
            <img src='pages/images/water2.png' width='150'>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.markdown("# Water Conservation Utility Guide")
    st.markdown("**Based on data from [EBMUD](https://www.ebmud.com/water/water-rates/rates-and-fees-schedules)**")
    st.write("Input your household information below to estimate your water usage and see potential savings by adopting water conservation habits.")

    # Input Data
    st.subheader("Household Information")
    household_size = st.number_input("Number of People in the House", min_value=1, value=3)

    # Shower usage
    avg_shower_duration = st.number_input("Average Shower Duration (minutes)", min_value=1, value=8)
    showers_per_day = st.number_input("Showers per Day per Person", min_value=1, max_value=30, value=1)

    # Lawn and pool inputs
    lawn_size = st.number_input("Size of Lawn (sq ft)", min_value=0, value=500)
    lawn_watering_frequency = st.slider("How many times do you water your lawn per week?", 0, 7, 3)
    has_pool = st.selectbox("Do you have a pool?", ("Yes", "No"))

    if has_pool == "Yes":
        pool_volume = st.number_input("Volume of the pool (gallons)", min_value=500, value=10000)
        pool_renew_frequency = st.slider("How often do you clean/renew pool water? (times per month)", 0, 4, 1)
    else:
        pool_volume = 0
        pool_renew_frequency = 0

    # Laundry
    laundry_per_week = st.number_input("Loads of Laundry per Week", min_value=0, value=5)

    # Car washing
    washes_car = st.selectbox("Do you wash your car at home?", ("Yes", "No"))
    if washes_car == "Yes":
        car_washes_per_week = st.number_input("Number of Car Washes per Week", min_value=0, max_value=99, value=1)
    else:
        car_washes_per_week = 0

    # Constants for calculation
    avg_daily_usage_per_person = 100  # gallons per day per person
    lawn_watering_rate = 0.62  # gallons per sq ft per watering
    pool_evaporation_rate = 0.003  # approx 0.3% of pool volume lost daily
    water_per_shower_minute = 2.1  # average gallons per minute for a shower
    water_per_laundry_load = 30  # average gallons per laundry load
    water_per_car_wash = 40  # average gallons per car wash

    # Calculate water usage
    people_usage = household_size * avg_daily_usage_per_person
    shower_usage = household_size * avg_shower_duration * showers_per_day * water_per_shower_minute * 7
    lawn_usage = lawn_size * lawn_watering_rate * lawn_watering_frequency
    pool_usage = pool_volume * pool_evaporation_rate * 7 + (pool_renew_frequency * pool_volume / 4)  # weekly pool usage
    laundry_usage = laundry_per_week * water_per_laundry_load
    car_wash_usage = car_washes_per_week * water_per_car_wash

    total_weekly_usage = people_usage * 7 + shower_usage + lawn_usage + pool_usage + laundry_usage + car_wash_usage
    total_monthly_usage = total_weekly_usage * 4  # estimate for 4 weeks in a month

    # Estimation of Bill Impact
    rate_per_gallon = 0.005  # example rate in dollars per gallon
    estimated_monthly_bill = total_monthly_usage * rate_per_gallon
    estimated_weekly_bill = total_weekly_usage * rate_per_gallon

    # Display usage and bill estimates with buttons
    st.subheader("Estimated Water Usage")
    if st.button("Estimate Weekly"):
        st.write(f"Estimated Weekly Water Usage: {total_weekly_usage:.2f} gallons")
        st.write(f"Estimated Weekly Water Bill: ${estimated_weekly_bill:.2f}")
    elif st.button("Estimate Monthly"):
        st.write(f"Estimated Monthly Water Usage: {total_monthly_usage:.2f} gallons")
        st.write(f"Estimated Monthly Water Bill: ${estimated_monthly_bill:.2f}")

    # Fun facts about water usage
    if total_weekly_usage or total_monthly_usage:
        st.subheader("Fun Facts About Your Water Usage")
        swimming_pools = total_monthly_usage / 20000  # assuming average pool volume of 20,000 gallons
        wildfire_extinguish = total_monthly_usage / 2500  # approx water usage to put off a small wildfire

        st.write(f"🌊 Your monthly water usage is equivalent to filling about {swimming_pools:.2f} average-sized swimming pools!")
        st.write(f"🔥 This amount of water could be used to help extinguish about {wildfire_extinguish:.2f} small wildfires.")

    # Tips & Tricks Button with API-Generated Advice
    if st.button("Possible Solutions"):
        st.subheader("Tips for Reducing Water and Waste")
        
        # Generate dynamic advice based on OpenAI's API
        prompt = (
            "Provide tips and practical advice on reducing household water usage. "
            "Consider factors such as lawn watering, pool maintenance, shower length, laundry, and car washing."
        )
        
        advice = generate_water_saving_advice(prompt)
        st.write(advice)

    # Customize interactivity for users
    st.write("For more personalized solutions, try adjusting the values in the calculator.")

if __name__ == "__main__":
    main()
