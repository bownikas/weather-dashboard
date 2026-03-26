import streamlit as st
import requests
import time
import folium
from streamlit_folium import st_folium

st.title("🌦️ Live Weather Dashboard")

city = st.text_input("Enter City / Area", "Chennai")

placeholder = st.empty()

while True:
    if city.strip() != "":
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

                with placeholder.container():

                    col1, col2 = st.columns([2, 1])

                    # ---------------- MAP ----------------
                    with col1:
                        st.subheader("🗺️ Live Map View")

                        m = folium.Map(
                            location=[lat, lon],
                            zoom_start=10,
                            tiles="OpenStreetMap"
                        )

                        folium.Marker(
                            [lat, lon],
                            popup=f"{location}, {country}",
                            tooltip="Click for details",
                            icon=folium.Icon(color="red", icon="info-sign")
                        ).add_to(m)

                        st_folium(m, width=700, height=450)

                    # ---------------- DETAILS ----------------
                    with col2:
                        st.subheader("🌦️ Weather Details")

                        st.write(f"📍 **Location:** {location}, {country}")
                        st.write(f"🌐 **Latitude:** {lat}")
                        st.write(f"🌐 **Longitude:** {lon}")

                        st.metric("🌡️ Temperature", f"{weather['temperature']} °C")
                        st.metric("🌬️ Wind Speed", f"{weather['windspeed']} km/h")
                        st.metric("🧭 Wind Direction", f"{weather['winddirection']}°")

                        st.caption("🔄 Auto refresh every 10 seconds")

            else:
                st.warning("Location not found")

        except Exception as e:
            st.error(f"Error: {e}")

    time.sleep(10)
