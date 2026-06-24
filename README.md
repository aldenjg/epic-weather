# City Weather Dashboard

A beginner-friendly Python web app that shows current weather for any city. Built with [Streamlit](https://streamlit.io/) and the [OpenWeather Current Weather API](https://openweathermap.org/current).

## What it does

Enter a city name, choose Celsius or Fahrenheit, and click **Get weather** to see live conditions including temperature, humidity, wind speed, and a weather icon.

## Features

- Search weather by city name
- Choose Celsius (metric) or Fahrenheit (imperial) units
- View city name, country, and weather description
- See OpenWeather weather icons
- Dashboard-style layout with temperature, feels-like, humidity, and wind speed
- Friendly error messages for common problems (missing city, invalid API key, city not found, network errors)

## Project structure

```
francis-python/
├── app.py                        # Main Streamlit application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── .gitignore                    # Files to exclude from git
└── .streamlit/
    └── secrets.toml.example      # Template for your API key (copy to secrets.toml)
```

## Prerequisites

- Python 3.9 or newer
- pip (Python package installer)
- A free OpenWeather API key (see below)

## How to get an OpenWeather API key

1. Go to [https://openweathermap.org/](https://openweathermap.org/) and create a free account.
2. Sign in and open your [API keys page](https://home.openweathermap.org/api_keys).
3. Copy your default API key (or create a new one).
4. New keys can take a few minutes to activate — wait before testing.

## Installation

Open a terminal in the project folder and run:

```bash
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Set up your API key

Streamlit reads secrets from a local file that is **not** committed to git.

1. Copy the example secrets file:

   ```bash
   cp .streamlit/secrets.toml.example .streamlit/secrets.toml
   ```

2. Open `.streamlit/secrets.toml` in a text editor.

3. Replace `your_api_key_here` with your real OpenWeather API key:

   ```toml
   OPENWEATHER_API_KEY = "paste_your_key_here"
   ```

**Important:** Never commit `.streamlit/secrets.toml` to git. It is listed in `.gitignore` for your safety.

## Run the app

With your virtual environment activated and your API key in place:

```bash
streamlit run app.py
```

Your browser should open automatically. If not, go to the URL shown in the terminal (usually `http://localhost:8501`).

## Troubleshooting

### Invalid or missing API key

- Make sure `.streamlit/secrets.toml` exists (copied from the example file).
- Check that your key is pasted correctly with no extra spaces.
- Confirm the key is active on your OpenWeather account (new keys may take up to 2 hours).

### City not found

- Check the spelling of the city name.
- Try adding the country code, for example: `London, GB` or `Paris, FR`.

### Missing Streamlit secret

If you see a message about a missing API key, you have not created `.streamlit/secrets.toml` yet. Follow the **Set up your API key** steps above.

### Network or timeout errors

- Check your internet connection.
- Try again in a few moments — the weather service may be temporarily unavailable.

## Deploy to Streamlit Community Cloud (optional)

You can host this app for free on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. Push your project to a GitHub repository (do **not** include `secrets.toml`).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Click **New app** and select your repository.
4. Set the main file path to `app.py`.
5. In **Advanced settings → Secrets**, paste:

   ```toml
   OPENWEATHER_API_KEY = "your_actual_api_key"
   ```

6. Click **Deploy**.

## License

This project is for learning purposes. OpenWeather data is subject to [OpenWeather's terms of use](https://openweathermap.org/terms).
