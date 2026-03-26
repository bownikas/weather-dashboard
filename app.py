import streamlit as st
import requests
import pandas as pd
import pydeck as pdk

st.title("🌦️ Live Weather Dashboard")

city = st.text_input("Enter City / Area", "Chennai")

if city:

    try:
        # ---------------- GEO LOCATION (IMPROVED) ----------------
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=5"
        geo_response = requests.get(geo_url).json()

        if "results" in geo_response and len(geo_response["results"]) > 0:

            # 🔥 Take best match (first result but safer now)
            result = geo_response["results"][0]

            lat = result["latitude"]
            lon = result["longitude"]
            location = result["name"]
            country = result.get("country", "Unknown")

            # ---------------- WEATHER ----------------
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_data = requests.get(weather_url).json()
            weather = weather_data["current_weather"]

            col1, col2 = st.columns([2, 1])

            # ---------------- MAP ----------------
            with col1:
                st.subheader("📍 Live Map")

                df = pd.DataFrame({
                    "lat": [lat],
                    "lon": [lon]
                })

                st.pydeck_chart(pdk.Deck(
                    map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
                    initial_view_state=pdk.ViewState(
                        latitude=lat,
                        longitude=lon,
                        zoom=10
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=df,
                            get_position='[lon, lat]',
                            get_color='[0, 120, 255, 220]',
                            get_radius=600,
                        )
                    ]
                ))

            # ---------------- DETAILS ----------------
            with col2:
                st.subheader("🌦️ Weather Info")

                st.write(f"📍 **{location}, {country}**")
                st.write(f"🌐 Latitude: {lat}")
                st.write(f"🌐 Longitude: {lon}")

                st.metric("🌡️ Temperature", f"{weather['temperature']} °C")
                st.metric("🌬️ Wind Speed", f"{weather['windspeed']} km/h")
                st.metric("🧭 Wind Direction", f"{weather['winddirection']}°")

        else:
            st.warning("❌ Location not found. Try another name.")

    except Exception as e:
        st.error(f"Error: {e}")
