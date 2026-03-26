import streamlit as st
import requests
import time

st.title("🌦️ Live Weather Dashboard")

city = st.text_input("Enter City / Area", "Chennai")

placeholder = st.empty()

while True:
    if city.strip() != "":
        try:
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_response = requests.get(geo_url).json()

            if "results" in geo_response:
                result = geo_response["results"][0]
                lat = result["latitude"]
                lon = result["longitude"]
                location = result["name"]

                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_data = requests.get(weather_url).json()

                weather = weather_data["current_weather"]

                with placeholder.container():
                    st.success(f"Live Weather in {location}")
                    st.write(f"🌡️ Temp: {weather['temperature']} °C")
                    st.write(f"🌬️ Wind: {weather['windspeed']} km/h")
                    st.write(f"🧭 Direction: {weather['winddirection']}°")

        except:
            st.error("Error fetching data")

    time.sleep(10)  # refresh every 10 seconds
