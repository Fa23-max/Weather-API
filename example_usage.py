"""
Example usage of the Weather API
This demonstrates how to use the API in your own applications
"""
import requests
import json


class WeatherClient:
    """Simple client for the Weather API"""
    
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
    
    def get_weather(self, location, unit='metric', format='simple'):
        """
        Get weather data for a location
        
        Args:
            location (str): Location name (e.g., "London,UK")
            unit (str): Unit system - 'metric', 'us', or 'uk'
            format (str): Response format - 'simple' or 'full'
            
        Returns:
            dict: Weather data or None if error
        """
        try:
            url = f"{self.base_url}/weather/{location}"
            params = {'unit': unit, 'format': format}
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code}")
                print(response.json())
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def get_current_temperature(self, location, unit='metric'):
        """Get just the current temperature for a location"""
        data = self.get_weather(location, unit=unit)
        if data and 'data' in data:
            return data['data']['current']['temperature']
        return None
    
    def get_forecast(self, location, days=7, unit='metric'):
        """Get weather forecast for a location"""
        data = self.get_weather(location, unit=unit)
        if data and 'data' in data:
            return data['data']['forecast'][:days]
        return None


# Example 1: Simple usage
def example_simple():
    """Simple example - get current weather"""
    print("Example 1: Simple Usage")
    print("-" * 60)
    
    client = WeatherClient()
    weather = client.get_weather("London,UK")
    
    if weather:
        current = weather['data']['current']
        print(f"Location: {weather['data']['location']}")
        print(f"Temperature: {current['temperature']}°C")
        print(f"Conditions: {current['conditions']}")
        print(f"Humidity: {current['humidity']}%")
        print(f"Wind Speed: {current['wind_speed']} km/h")


# Example 2: Get just the temperature
def example_temperature():
    """Get just the temperature"""
    print("\n\nExample 2: Get Temperature Only")
    print("-" * 60)
    
    client = WeatherClient()
    
    cities = ["London,UK", "New York", "Tokyo", "Paris"]
    
    for city in cities:
        temp = client.get_current_temperature(city)
        if temp:
            print(f"{city}: {temp}°C")


# Example 3: Get forecast
def example_forecast():
    """Get weather forecast"""
    print("\n\nExample 3: Weather Forecast")
    print("-" * 60)
    
    client = WeatherClient()
    forecast = client.get_forecast("Paris", days=5)
    
    if forecast:
        print("5-Day Forecast for Paris:")
        for day in forecast:
            print(f"\n{day['date']}:")
            print(f"  High: {day['temp_max']}°C")
            print(f"  Low: {day['temp_min']}°C")
            print(f"  Conditions: {day['conditions']}")
            print(f"  Precipitation: {day['precipitation_prob']}%")


# Example 4: Compare temperatures in different units
def example_units():
    """Compare temperatures in different units"""
    print("\n\nExample 4: Different Unit Systems")
    print("-" * 60)
    
    client = WeatherClient()
    location = "New York"
    
    # Metric
    weather_metric = client.get_weather(location, unit='metric')
    temp_c = weather_metric['data']['current']['temperature']
    
    # US
    weather_us = client.get_weather(location, unit='us')
    temp_f = weather_us['data']['current']['temperature']
    
    print(f"Temperature in {location}:")
    print(f"  Metric: {temp_c}°C")
    print(f"  US: {temp_f}°F")


# Example 5: Error handling
def example_error_handling():
    """Demonstrate error handling"""
    print("\n\nExample 5: Error Handling")
    print("-" * 60)
    
    client = WeatherClient()
    
    # Invalid location
    print("Testing invalid location...")
    weather = client.get_weather("InvalidCityXYZ123")
    if not weather:
        print("Handled error gracefully")


# Example 6: Batch requests
def example_batch():
    """Get weather for multiple cities"""
    print("\n\nExample 6: Batch Requests")
    print("-" * 60)
    
    client = WeatherClient()
    
    cities = [
        "London,UK",
        "Paris,France",
        "Berlin,Germany",
        "Madrid,Spain",
        "Rome,Italy"
    ]
    
    print("European Cities Weather:")
    for city in cities:
        weather = client.get_weather(city)
        if weather:
            current = weather['data']['current']
            print(f"\n{weather['data']['location']}:")
            print(f"  {current['temperature']}°C - {current['conditions']}")


if __name__ == "__main__":
    print("="*60)
    print("Weather API - Example Usage")
    print("="*60)
    print("\nMake sure the API is running: python app.py\n")
    
    try:
        # Run all examples
        example_simple()
        example_temperature()
        example_forecast()
        example_units()
        example_error_handling()
        example_batch()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the API is running with: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
