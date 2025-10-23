"""
Quick setup script to create .env file with your API key
"""
import os

def create_env_file():
    """Create .env file with the provided API key"""
    
    api_key = "Weather api"
    
    env_content = f"""# Visual Crossing Weather API Key
WEATHER_API_KEY={api_key}

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Cache Configuration (in seconds)
CACHE_EXPIRATION=43200

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000

# Rate Limiting
RATE_LIMIT=100 per hour
"""
    
    env_path = ".env"
    
    if os.path.exists(env_path):
        response = input(".env file already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    print(f"✅ API Key set to: {api_key}")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. (Optional) Start Redis server")
    print("3. Start the API: python app.py")
    print("4. Test the API: python test_api.py")


if __name__ == "__main__":
    create_env_file()
