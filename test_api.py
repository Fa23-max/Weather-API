"""
Simple test script for the Weather API
Run this after starting the API server with: python app.py
"""
import requests
import json
import time


def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))


def main():
    base_url = "http://localhost:5000"
    
    print("Testing Weather API...")
    
    # Test 1: API Home
    print("\n1. Testing API Home...")
    response = requests.get(f"{base_url}/")
    print_response("API Home", response)
    
    # Test 2: Health Check
    print("\n2. Testing Health Check...")
    response = requests.get(f"{base_url}/health")
    print_response("Health Check", response)
    
    # Test 3: Get Weather (First request - should fetch from API)
    print("\n3. Testing Weather Request (Fresh Data)...")
    response = requests.get(f"{base_url}/weather/London,UK")
    print_response("Weather for London, UK", response)
    
    # Test 4: Get Weather (Second request - should be cached)
    print("\n4. Testing Weather Request (Cached Data)...")
    time.sleep(1)  # Small delay
    response = requests.get(f"{base_url}/weather/London,UK")
    print_response("Weather for London, UK (Cached)", response)
    
    # Test 5: Different location with US units
    print("\n5. Testing Weather with US Units...")
    response = requests.get(f"{base_url}/weather/New York?unit=us")
    print_response("Weather for New York (US Units)", response)
    
    # Test 6: Cache Statistics
    print("\n6. Testing Cache Statistics...")
    response = requests.get(f"{base_url}/cache/stats")
    print_response("Cache Statistics", response)
    
    # Test 7: Invalid location
    print("\n7. Testing Invalid Location...")
    response = requests.get(f"{base_url}/weather/InvalidCityXYZ123")
    print_response("Invalid Location", response)
    
    # Test 8: Full format
    print("\n8. Testing Full Format Response...")
    response = requests.get(f"{base_url}/weather/Paris?format=full")
    print_response("Weather for Paris (Full Format)", response)
    
    print("\n" + "="*60)
    print("All tests completed!")
    print("="*60)


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API server.")
        print("Make sure the API is running with: python app.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
