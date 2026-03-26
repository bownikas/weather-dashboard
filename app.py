import streamlit as st
import requests

st.title("🌦️ Weather Dashboard")

API_KEY = st.secrets["API_KEY"]

city = st.text_input("Enter City Name", "Chennai")

if st.button("Get Weather"):
    if city.strip() == "":
        st.warning("Please enter a city name")
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get("cod") == 200:
            st.success(f"Weather in {data['name']}")
            st.write(f"🌡️ Temp: {data['main']['temp']} °C")
            st.write(f"💧 Humidity: {data['main']['humidity']}%")
            st.write(f"🌬️ Wind: {data['wind']['speed']} m/s")
        else:
            st.error("City not found or API issue")
