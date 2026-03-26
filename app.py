import streamlit as st
import requests

st.title("🌦️ Weather Dashboard (Area-wise)")

city = st.text_input("Enter City / Area", "Chennai")

if st.button("Get Weather"):
    
    if city.strip() == "":
        st.warning("Please enter a city or area name")
    
    else:
        try:
            # Step 1: Get latitude & longitude (accurate result)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
            geo_response = requests.get(geo_url).json()

            if "results" not in geo_response:
                st.error("❌ Area not found. Try a different name")
            
            else:
                result = geo_response["results"][0]
                lat = result["latitude"]
                lon = result["longitude"]
                location_name = result["name"]
                country = result.get("country", "")

                # Step 2: Get weather data
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_response = requests.get(weather_url).json()

                weather = weather_response["current_weather"]

                # Display results
                st.success(f"Weather in {location_name}, {country}")
                st.write(f"📍 Latitude: {lat}, Longitude: {lon}")
                st.write(f"🌡️ Temperature: {weather['temperature']} °C")
                st.write(f"🌬️ Wind Speed: {weather['windspeed']} km/h")
                st.write(f"🧭 Wind Direction: {weather['winddirection']}°")

        except Exception as e:
            st.error("⚠️ Something went wrong. Please try again.")
