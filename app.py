import streamlit as st
import requests

st.title("🌦️ Weather Dashboard")

API_KEY = st.secrets["7e9c04257efca0ae3b5a708436f6403a"]

# User input
city = st.text_input("Enter City Name", "Chennai")

# Button click
if st.button("Get Weather"):
    
    if city.strip() == "":
        st.warning("Please enter a city name")
    
    else:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        
        try:
            response = requests.get(url)
            data = response.json()

            if data.get("cod") == 200:
                st.success(f"Weather in {data['name']}, {data['sys']['country']}")
                
                st.write(f"🌡️ Temperature: {data['main']['temp']} °C")
                st.write(f"💧 Humidity: {data['main']['humidity']}%")
                st.write(f"🌬️ Wind Speed: {data['wind']['speed']} m/s")
                st.write(f"🌥️ Condition: {data['weather'][0]['description']}")
            
            else:
                st.error("❌ City not found. Try again with correct spelling")

        except Exception as e:
            st.error("⚠️ Something went wrong. Check your API or internet connection")
