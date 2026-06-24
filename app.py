"""City Weather Dashboard — a simple Streamlit app for current weather."""

from datetime import datetime, timedelta, timezone
from typing import Any

import requests
import streamlit as st

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT = 10

# Map user-friendly unit labels to OpenWeather API unit parameters
UNIT_MAP = {
    "Celsius": "metric",
    "Fahrenheit": "imperial",
}


@st.cache_data(ttl=600, show_spinner=False)
def get_weather(city: str, units: str, api_key: str) -> dict[str, Any]:
    """Fetch current weather for a city from the OpenWeather API."""
    params = {
        "q": city,
        "appid": api_key,
        "units": units,
    }
    response = requests.get(OPENWEATHER_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()


def local_time_from_epoch(epoch_seconds: int, tz_offset_seconds: int) -> str:
    """Format a UTC epoch timestamp as the city's local HH:MM time."""
    utc_time = datetime.fromtimestamp(epoch_seconds, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=tz_offset_seconds)
    return local_time.strftime("%H:%M")


def display_weather(data: dict[str, Any], unit_label: str) -> None:
    """Render weather data as a small dashboard."""
    city_name = data["name"]
    country = data["sys"]["country"]
    description = data["weather"][0]["description"].capitalize()
    icon_code = data["weather"][0]["icon"]
    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    pressure = data["main"]["pressure"]
    wind_speed = data["wind"]["speed"]
    tz_offset = data.get("timezone", 0)
    sunrise = local_time_from_epoch(data["sys"]["sunrise"], tz_offset)
    sunset = local_time_from_epoch(data["sys"]["sunset"], tz_offset)

    # Choose display symbols based on selected units
    if unit_label == "Celsius":
        temp_unit = "°C"
        wind_unit = "m/s"
    else:
        temp_unit = "°F"
        wind_unit = "mph"

    st.subheader(f"{city_name}, {country}")
    st.write(description)

    icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
    st.image(icon_url, width=100)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Temperature", f"{temp:.1f}{temp_unit}")
    col2.metric("Feels like", f"{feels_like:.1f}{temp_unit}")
    col3.metric("Humidity", f"{humidity}%")
    col4.metric("Wind speed", f"{wind_speed} {wind_unit}")

    col5, col6, col7 = st.columns(3)
    col5.metric("Pressure", f"{pressure} hPa")
    col6.metric("Sunrise", sunrise)
    col7.metric("Sunset", sunset)


# --- Page setup ---
st.set_page_config(
    page_title="City Weather Dashboard",
    page_icon="🌤️",
    layout="centered",
)

st.title("City Weather Dashboard")
st.write(
    "Enter a city name, choose Celsius or Fahrenheit, then click "
    "**Get weather** to see the current conditions."
)

with st.form("weather_form"):
    city = st.text_input("City name", placeholder="e.g. London")
    unit_label = st.selectbox("Temperature units", ["Celsius", "Fahrenheit"])
    get_weather_clicked = st.form_submit_button("Get weather")

if get_weather_clicked:
    if not city.strip():
        st.warning("Please enter a city name.")
    else:
        # Read API key from Streamlit secrets
        try:
            api_key = st.secrets["OPENWEATHER_API_KEY"]
        except (KeyError, FileNotFoundError):
            st.error(
                "OpenWeather API key not found. Copy "
                "`.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` "
                "and add your API key."
            )
        else:
            if not api_key or api_key == "your_api_key_here":
                st.error(
                    "Invalid or missing API key. Add your OpenWeather API key to "
                    "`.streamlit/secrets.toml`."
                )
            else:
                units = UNIT_MAP[unit_label]

                try:
                    with st.spinner("Fetching weather..."):
                        weather_data = get_weather(city.strip(), units, api_key)
                    display_weather(weather_data, unit_label)

                except requests.exceptions.Timeout:
                    st.error(
                        "The request timed out. Check your internet connection and try again."
                    )
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to the weather service. "
                        "Check your internet connection and try again."
                    )
                except requests.exceptions.HTTPError as err:
                    status_code = err.response.status_code if err.response is not None else None
                    if status_code == 401:
                        st.error(
                            "Invalid API key. Check that your key is correct in "
                            "`.streamlit/secrets.toml`."
                        )
                    elif status_code == 404:
                        st.error(
                            f"City '{city.strip()}' was not found. "
                            "Try a different spelling or add the country (e.g. 'Paris, FR')."
                        )
                    else:
                        st.error(
                            "Something went wrong while fetching the weather. Please try again."
                        )
                except (KeyError, IndexError, TypeError):
                    st.error(
                        "Received an unexpected response from the weather service. "
                        "Please try again later."
                    )
                except Exception:
                    st.error("An unexpected error occurred. Please try again later.")
