"""Weather tool implementation for the chatbot."""

import os
import requests
from typing import Dict, Any, Optional
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a specified city.
    
    Args:
        city: The name of the city to get weather for
        
    Returns:
        A formatted string with current weather information
    """
    # For demo purposes, we'll use a free weather API
    # In production, you'd want to use OpenWeatherMap with an API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    
    if api_key:
        return _get_weather_from_openweather(city, api_key)
    else:
        # Fallback to a free service that doesn't require API key
        return _get_weather_from_wttr(city)


def _get_weather_from_openweather(city: str, api_key: str) -> str:
    """Get weather from OpenWeatherMap API."""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        weather_info = (
            f"Current weather in {data['name']}, {data['sys']['country']}:
            f"Temperature: {data['main']['temp']}°C (feels like {data['main']['feels_like']}°C)
            f"Condition: {data['weather'][0]['description'].title()}
            f"Humidity: {data['main']['humidity']}%
            f"Wind: {data['wind'].get('speed', 0)} m/s"
        )
        
        return weather_info
        
    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't fetch weather data for {city}. Please check the city name and try again."
    except KeyError as e:
        return f"Sorry, I received unexpected data format for {city}. Please try again."


def _get_weather_from_wttr(city: str) -> str:
    """Get weather from wttr.in (free service, no API key required)."""
    try:
        # wttr.in provides a simple text-based weather service
        url = f"http://wttr.in/{city}?format=3"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        weather_text = response.text.strip()
        
        if "Unknown location" in weather_text or not weather_text:
            return f"Sorry, I couldn't find weather information for '{city}'. Please check the city name and try again."
        
        return f"Current weather: {weather_text}"
        
    except requests.exceptions.RequestException as e:
        return f"Sorry, I couldn't fetch weather data for {city} due to a network error. Please try again later."
    except Exception as e:
        return f"Sorry, I encountered an error while getting weather for {city}. Please try again."

