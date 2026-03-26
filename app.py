import streamlit as st
import requests
import time
import pydeck as pdk
import pandas as pd

st.title("🌦️ Live Weather Dashboard with Map")

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
                country = result.get("country", "Unknown")

                # ---------------- WEATHER ----------------
                weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                weather_data = requests.get(weather_url).json()
                weather = weather_data["current_weather"]

                # ---------------- UI ----------------
                with placeholder.container():

                    col1, col2 = st.columns([2, 1])

                    # MAP
                    with col1:
                        st.subheader("📍 Live Location Map")

                        df = pd.DataFrame({
                            "lat": [lat],
                            "lon": [lon]
                        })

                        st.pydeck_chart(pdk.Deck(
                            map_style="mapbox://styles/mapbox/streets-v11",
                            initial_view_state=pdk.ViewState(
                                latitude=lat,
                                longitude=lon,
                                zoom=10,
                                pitch=0
                            ),
                            layers=[
                                pdk.Layer(
                                    "ScatterplotLayer",
                                    data=df,
                                    get_position='[lon, lat]',
                                    get_color='[255, 0, 0, 200]',
                                    get_radius=300,
                                )
                            ],
                            tooltip={"text": f"{location}\nLat: {lat}\nLon: {lon}"}
                        ))

                    # DETAILS PANEL
                    with col2:
                        st.subheader("🌦️ Weather Details")

                        st.write(f"📍 **Location:** {location}, {country}")
                        st.write(f"🌐 **Latitude:** {lat}")
                        st.write(f"🌐 **Longitude:** {lon}")

                        st.metric("🌡️ Temperature", f"{weather['temperature']} °C")
                        st.metric("🌬️ Wind Speed", f"{weather['windspeed']} km/h")
                        st.metric("🧭 Wind Direction", f"{weather['winddirection']}°")

                        st.caption("🔄 Auto-refresh every 10 seconds")

            else:
                st.warning("Location not found")

        except Exception as e:
            st.error(f"Error: {e}")

    time.sleep(10)
