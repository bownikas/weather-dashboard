import streamlit as st
import requests
import pandas as pd

st.title("🌦️ Live Weather Dashboard")

city = st.text_input("Enter City / Area", "Chennai")

if city:

    try:
        # ---------------- GEO LOCATION ----------------
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo_response = requests.get(geo_url).json()

        if "results" in geo_response:

            result = geo_response["results"][0]

            lat = result["latitude"]
            lon = result["longitude"]
            location = result["name"]
            country = result.get("country", "")

            # ---------------- WEATHER ----------------
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_data = requests.get(weather_url).json()
            weather = weather_data["current_weather"]

            # ---------------- UI ----------------
            col1, col2 = st.columns([2, 1])

            # MAP
            with col1:
                st.subheader("📍 Live Location Map")

                map_data = pd.DataFrame({
                    "lat": [lat],
                    "lon": [lon]
                })

                st.map(map_data, zoom=10)

            # DETAILS
            with col2:
                st.subheader("🌦️ Weather Info")

                st.write(f"📍 **{location}, {country}**")
                st.write(f"🌐 Latitude: {lat}")
                st.write(f"🌐 Longitude: {lon}")

                st.metric("🌡️ Temperature", f"{weather['temperature']} °C")
                st.metric("🌬️ Wind Speed", f"{weather['windspeed']} km/h")
                st.metric("🧭 Wind Direction", f"{weather['winddirection']}°")

        else:
            st.warning("Location not found")

    except Exception as e:
        st.error(f"Error: {e}")
