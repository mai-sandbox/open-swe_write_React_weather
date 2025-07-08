"""Weather tool implementation for LangGraph chatbot."""

import os
import logging
from typing import Dict, Any
import requests
from langchain_core.tools import tool

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def get_weather(city: str) -> str:
    """
    Get current weather information for a specified city.
    
    This tool fetches weather data from OpenWeatherMap API and returns
    formatted weather information including temperature, description,
    humidity, and wind speed.
    
    Args:
        city: The name of the city to get weather information for
        
    Returns:
        A formatted string containing weather information for the city
        
    Raises:
        Exception: If API call fails or city is not found
    """
    try:
        # Get API key from environment variable
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            logger.error("OpenWeatherMap API key not found in environment variables")
            return "Error: Weather service is not configured. Please set OPENWEATHER_API_KEY environment variable."
        
        # Validate input
        if not city or not city.strip():
            return "Error: Please provide a valid city name."
        
        city = city.strip()
        
        # OpenWeatherMap API endpoint
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"  # Use Celsius
        }
        
        logger.info(f"Fetching weather data for city: {city}")
        
        # Make API request
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 404:
            return f"Error: City '{city}' not found. Please check the spelling and try again."
        elif response.status_code == 401:
            logger.error("Invalid API key")
            return "Error: Weather service authentication failed."
        elif response.status_code != 200:
            logger.error(f"API request failed with status code: {response.status_code}")
            return "Error: Unable to fetch weather data. Service temporarily unavailable."
        
        # Parse response
        data: Dict[str, Any] = response.json()
        
        # Extract weather information
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]
        
        # Format weather information
        weather_info = f"""🌤️ Weather in {city.title()}:
• Temperature: {temperature}°C (feels like {feels_like}°C)
• Conditions: {description}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s"""
        
        logger.info(f"Successfully retrieved weather data for {city}")
        return weather_info
        
    except requests.exceptions.Timeout:
        logger.error("Request timeout while fetching weather data")
        return "Error: Weather service request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        logger.error("Connection error while fetching weather data")
        return "Error: Unable to connect to weather service. Please check your internet connection."
    except KeyError as e:
        logger.error(f"Unexpected API response format: {e}")
        return "Error: Received unexpected response from weather service."
    except Exception as e:
        logger.error(f"Unexpected error in get_weather: {e}")
        return "Error: An unexpected error occurred while fetching weather data."


