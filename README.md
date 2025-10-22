# Weather API

A production-ready Weather API that fetches and caches weather data from Visual Crossing's Weather API. This project demonstrates working with 3rd party APIs, Redis caching, environment variables, and rate limiting.

## Features

- ✅ **3rd Party API Integration** - Fetches real-time weather data from Visual Crossing
- ✅ **Redis Caching** - Intelligent caching with automatic expiration (default: 12 hours)
- ✅ **Rate Limiting** - Prevents API abuse (default: 100 requests per hour)
- ✅ **Environment Variables** - Secure configuration management
- ✅ **Error Handling** - Comprehensive error handling for all edge cases
- ✅ **Multiple Unit Systems** - Support for metric, US, and UK units
- ✅ **Graceful Degradation** - Works even if Redis is unavailable
- ✅ **Logging** - Detailed logging for debugging and monitoring

## Prerequisites

- Python 3.8 or higher
- Redis server (optional but recommended)
- Visual Crossing API key (free tier available)

## Installation

### 1. Clone or navigate to the project directory

```bash
cd "c:/Users/Admin/Documents/projects/Weather Api"
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Set up environment variables

Copy the example environment file:
```bash
copy .env.example .env
```

Edit `.env` and add your Visual Crossing API key:
```env
WEATHER_API_KEY=your_actual_api_key_here
```

**Get your free API key:** https://www.visualcrossing.com/weather-api

### 6. Install and start Redis (optional but recommended)

**Windows:**
- Download Redis from: https://github.com/microsoftarchive/redis/releases
- Or use Docker: `docker run -d -p 6379:6379 redis:alpine`

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

**Mac:**
```bash
brew install redis
brew services start redis
```

**Note:** The API will work without Redis, but caching will be disabled.

## Usage

### Start the API server

```bash
python app.py
```

The API will be available at: `http://localhost:5000`

### API Endpoints

#### 1. Home / API Information
```
GET /
```
Returns API information and usage instructions.

#### 2. Get Weather Data
```
GET /weather/<location>
```

**Parameters:**
- `location` (required): City name or location (e.g., "London,UK", "New York", "Paris,France")
- `unit` (optional): Unit system - `metric` (default), `us`, or `uk`
- `format` (optional): Response format - `simple` (default) or `full`

**Examples:**
```bash
# Simple format with metric units (default)
curl http://localhost:5000/weather/London,UK

# US units
curl http://localhost:5000/weather/New%20York?unit=us

# Full format
curl http://localhost:5000/weather/Tokyo?format=full

# UK units
curl http://localhost:5000/weather/Manchester?unit=uk
```

**Response (simple format):**
```json
{
  "location": "London,UK",
  "cached": false,
  "data": {
    "location": "London, England, United Kingdom",
    "timezone": "Europe/London",
    "current": {
      "datetime": "14:30:00",
      "temperature": 18.5,
      "feels_like": 17.2,
      "humidity": 65,
      "conditions": "Partly cloudy",
      "description": "Partly cloudy throughout the day.",
      "wind_speed": 15.5,
      "pressure": 1013.2,
      "visibility": 10.0,
      "uv_index": 4
    },
    "forecast": [
      {
        "date": "2025-10-22",
        "temp_max": 20.5,
        "temp_min": 12.3,
        "temp_avg": 16.4,
        "conditions": "Partly cloudy",
        "description": "Partly cloudy throughout the day.",
        "precipitation_prob": 20,
        "humidity": 65,
        "wind_speed": 15.5
      }
    ]
  }
}
```

#### 3. Health Check
```
GET /health
```
Returns API health status and cache statistics.

#### 4. Cache Statistics
```
GET /cache/stats
```
Returns cache statistics (hits, misses, total keys).

#### 5. Clear Cache
```
DELETE /cache/clear
```
Clears all cached data.

## Configuration

All configuration is done through environment variables in the `.env` file:

| Variable | Description | Default |
|----------|-------------|---------|
| `WEATHER_API_KEY` | Visual Crossing API key | (required) |
| `REDIS_HOST` | Redis server host | localhost |
| `REDIS_PORT` | Redis server port | 6379 |
| `REDIS_PASSWORD` | Redis password (if required) | (empty) |
| `REDIS_DB` | Redis database number | 0 |
| `CACHE_EXPIRATION` | Cache expiration in seconds | 43200 (12 hours) |
| `FLASK_ENV` | Flask environment | development |
| `FLASK_DEBUG` | Enable debug mode | True |
| `PORT` | API server port | 5000 |
| `RATE_LIMIT` | Rate limit per IP | 100 per hour |

## How It Works

### Caching Strategy

1. When a weather request is made, the API first checks Redis cache using the key format: `weather:{location}:{unit}`
2. If data exists in cache and hasn't expired, it returns the cached data immediately
3. If cache miss, the API fetches fresh data from Visual Crossing API
4. The fresh data is cached with a TTL (Time To Live) of 12 hours by default
5. Redis automatically removes expired keys, keeping the cache clean

### Rate Limiting

- Rate limiting is applied per IP address
- Default: 100 requests per hour
- Uses Redis for distributed rate limiting (falls back to in-memory if Redis unavailable)
- Returns HTTP 429 when limit is exceeded

### Error Handling

The API handles various error scenarios:
- Invalid location → 400 Bad Request
- Invalid API key → 401 Unauthorized
- Weather API rate limit → 429 Too Many Requests
- Weather API timeout → 504 Gateway Timeout
- Weather API unavailable → 503 Service Unavailable
- Server errors → 500 Internal Server Error

## Testing

### Test with curl

```bash
# Basic request
curl http://localhost:5000/weather/London,UK

# With different units
curl http://localhost:5000/weather/Paris?unit=metric

# Check if caching works (second request should be faster)
curl http://localhost:5000/weather/Tokyo
curl http://localhost:5000/weather/Tokyo

# Check cache stats
curl http://localhost:5000/cache/stats

# Health check
curl http://localhost:5000/health
```

### Test with Python

```python
import requests

# Get weather
response = requests.get('http://localhost:5000/weather/London,UK')
print(response.json())

# Check cache stats
stats = requests.get('http://localhost:5000/cache/stats')
print(stats.json())
```

## Production Deployment

For production deployment, use a production WSGI server like Gunicorn:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

**Environment variables for production:**
```env
FLASK_ENV=production
FLASK_DEBUG=False
RATE_LIMIT=1000 per hour
```

## Project Structure

```
Weather Api/
├── app.py                 # Main Flask application
├── config.py              # Configuration management
├── cache.py               # Redis cache implementation
├── weather_service.py     # Weather API service
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Troubleshooting

### Redis Connection Error
If you see "Redis connection failed" in logs:
- Make sure Redis is installed and running
- Check Redis connection settings in `.env`
- The API will still work without Redis, but caching will be disabled

### Invalid API Key Error
- Make sure you've set `WEATHER_API_KEY` in your `.env` file
- Verify your API key is valid at https://www.visualcrossing.com/account

### Rate Limit Exceeded
- Wait for the rate limit window to reset (1 hour by default)
- Or increase `RATE_LIMIT` in `.env` file

## License

This project is open source and available for educational purposes.

## Resources

- Visual Crossing Weather API: https://www.visualcrossing.com/weather-api
- Redis Documentation: https://redis.io/documentation
- Flask Documentation: https://flask.palletsprojects.com/
- Flask-Limiter: https://flask-limiter.readthedocs.io/

https://roadmap.sh/projects/weather-api-wrapper-service