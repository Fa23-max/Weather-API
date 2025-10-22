import requests
import logging
from urllib.parse import quote
from config import Config

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for fetching weather data from Visual Crossing API"""
    
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.endpoint = Config.WEATHER_API_ENDPOINT
    
    def get_weather(self, location, unit_group='metric'):
        """
        Fetch weather data for a location
        
        Args:
            location (str): Location name (e.g., "London,UK" or "New York")
            unit_group (str): Unit system - 'metric', 'us', or 'uk'
            
        Returns:
            dict: Weather data or error information
        """
        try:
            # Encode location for URL
            encoded_location = quote(location)
            
            # Build the URL
            url = f"{self.endpoint}{encoded_location}"
            
            # Set query parameters
            params = {
                'unitGroup': unit_group,
                'contentType': 'json',
                'key': self.api_key
            }
            
            logger.info(f"Fetching weather data for location: {location}")
            
            # Make the request
            response = requests.get(url, params=params, timeout=10)
            
            # Check for HTTP errors
            if response.status_code == 400:
                logger.error(f"Bad request for location: {location}")
                return {
                    'error': 'Invalid location or parameters',
                    'status_code': 400
                }
            elif response.status_code == 401:
                logger.error("Invalid API key")
                return {
                    'error': 'Invalid API key',
                    'status_code': 401
                }
            elif response.status_code == 429:
                logger.error("Rate limit exceeded on weather API")
                return {
                    'error': 'Weather API rate limit exceeded. Please try again later.',
                    'status_code': 429
                }
            elif response.status_code != 200:
                logger.error(f"Weather API error: {response.status_code}")
                return {
                    'error': f'Weather API error: {response.status_code}',
                    'status_code': response.status_code
                }
            
            # Parse and return the data
            weather_data = response.json()
            logger.info(f"Successfully fetched weather data for: {location}")
            
            return {
                'success': True,
                'data': weather_data
            }
            
        except requests.exceptions.Timeout:
            logger.error("Weather API request timed out")
            return {
                'error': 'Weather API request timed out',
                'status_code': 504
            }
        except requests.exceptions.ConnectionError:
            logger.error("Failed to connect to weather API")
            return {
                'error': 'Failed to connect to weather API',
                'status_code': 503
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return {
                'error': f'Request error: {str(e)}',
                'status_code': 500
            }
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return {
                'error': f'Unexpected error: {str(e)}',
                'status_code': 500
            }
    
    def format_weather_response(self, weather_data):
        """
        Format weather data into a simplified response
        
        Args:
            weather_data (dict): Raw weather data from API
            
        Returns:
            dict: Formatted weather response
        """
        try:
            current = weather_data.get('currentConditions', {})
            days = weather_data.get('days', [])
            
            formatted = {
                'location': weather_data.get('resolvedAddress', 'Unknown'),
                'timezone': weather_data.get('timezone', 'UTC'),
                'current': {
                    'datetime': current.get('datetime', ''),
                    'temperature': current.get('temp', 0),
                    'feels_like': current.get('feelslike', 0),
                    'humidity': current.get('humidity', 0),
                    'conditions': current.get('conditions', ''),
                    'description': current.get('description', ''),
                    'wind_speed': current.get('windspeed', 0),
                    'pressure': current.get('pressure', 0),
                    'visibility': current.get('visibility', 0),
                    'uv_index': current.get('uvindex', 0)
                },
                'forecast': []
            }
            
            # Add forecast for next days
            for day in days[:7]:  # Limit to 7 days
                formatted['forecast'].append({
                    'date': day.get('datetime', ''),
                    'temp_max': day.get('tempmax', 0),
                    'temp_min': day.get('tempmin', 0),
                    'temp_avg': day.get('temp', 0),
                    'conditions': day.get('conditions', ''),
                    'description': day.get('description', ''),
                    'precipitation_prob': day.get('precipprob', 0),
                    'humidity': day.get('humidity', 0),
                    'wind_speed': day.get('windspeed', 0)
                })
            
            return formatted
            
        except Exception as e:
            logger.error(f"Error formatting weather data: {e}")
            return weather_data
