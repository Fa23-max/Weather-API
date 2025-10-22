# Useful Commands

Quick reference for common tasks.

## Setup Commands

### Create environment file
```bash
python setup_env.py
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Create virtual environment (optional)
```bash
python -m venv venv
venv\Scripts\activate
```

## Running the API

### Development mode
```bash
python app.py
```

### Production mode (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### With custom port
```bash
# Edit .env file and change PORT=5000 to desired port
python app.py
```

## Testing Commands

### Run test suite
```bash
python test_api.py
```

### Run example usage
```bash
python example_usage.py
```

### Test with curl

#### Get weather
```bash
curl http://localhost:5000/weather/London,UK
```

#### Get weather with US units
```bash
curl "http://localhost:5000/weather/New%20York?unit=us"
```

#### Get full format
```bash
curl "http://localhost:5000/weather/Tokyo?format=full"
```

#### Health check
```bash
curl http://localhost:5000/health
```

#### Cache statistics
```bash
curl http://localhost:5000/cache/stats
```

#### Clear cache
```bash
curl -X DELETE http://localhost:5000/cache/clear
```

### Test with Python

```python
import requests

# Get weather
response = requests.get('http://localhost:5000/weather/London,UK')
print(response.json())

# With parameters
response = requests.get('http://localhost:5000/weather/Paris', 
                       params={'unit': 'metric', 'format': 'simple'})
print(response.json())
```

### Test with PowerShell

```powershell
# Get weather
Invoke-RestMethod -Uri "http://localhost:5000/weather/London,UK"

# With parameters
Invoke-RestMethod -Uri "http://localhost:5000/weather/Paris?unit=metric"

# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

## Redis Commands

### Start Redis (Docker)
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Stop Redis (Docker)
```bash
docker stop redis
```

### Start Redis (Docker)
```bash
docker start redis
```

### Remove Redis container
```bash
docker rm -f redis
```

### Connect to Redis CLI (Docker)
```bash
docker exec -it redis redis-cli
```

### Redis CLI commands
```bash
# List all keys
KEYS *

# Get a specific key
GET weather:london,uk:metric

# Delete a key
DEL weather:london,uk:metric

# Check TTL (time to live)
TTL weather:london,uk:metric

# Get all keys count
DBSIZE

# Clear all keys
FLUSHDB
```

## Development Commands

### Check Python version
```bash
python --version
```

### List installed packages
```bash
pip list
```

### Update requirements.txt
```bash
pip freeze > requirements.txt
```

### Check for outdated packages
```bash
pip list --outdated
```

### Upgrade a package
```bash
pip install --upgrade flask
```

## Git Commands

### Initialize repository
```bash
git init
git add .
git commit -m "Initial commit: Weather API"
```

### Create .gitignore
Already created! The `.env` file is automatically ignored.

### Check status
```bash
git status
```

## Debugging Commands

### Check if port is in use (Windows)
```bash
netstat -ano | findstr :5000
```

### Kill process on port (Windows)
```bash
# Find PID from above command, then:
taskkill /PID <PID> /F
```

### Check Redis connection
```bash
# Using Python
python -c "import redis; r = redis.Redis(host='localhost', port=6379); print(r.ping())"
```

### Test Visual Crossing API directly
```bash
curl "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK?unitGroup=metric&contentType=json&key=YOUR_API_KEY"
```

### View logs in real-time
```bash
# Run the app and watch the console output
python app.py
```

## Environment Commands

### View environment variables
```bash
# Windows
type .env

# Linux/Mac
cat .env
```

### Edit environment variables
```bash
# Windows
notepad .env

# Linux/Mac
nano .env
```

### Validate configuration
```python
python -c "from config import Config; Config.validate(); print('Config OK')"
```

## Performance Testing

### Simple load test with curl
```bash
# Windows PowerShell
1..100 | ForEach-Object { Invoke-RestMethod -Uri "http://localhost:5000/weather/London,UK" }
```

### Using Apache Bench (if installed)
```bash
ab -n 100 -c 10 http://localhost:5000/weather/London,UK
```

## Maintenance Commands

### Clear Python cache
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Linux/Mac
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Backup .env file
```bash
copy .env .env.backup
```

### Check disk space (Redis data)
```bash
docker exec redis redis-cli INFO memory
```

## Useful API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/weather/<location>` | Get weather |
| GET | `/cache/stats` | Cache statistics |
| DELETE | `/cache/clear` | Clear cache |

## Common Locations to Test

```bash
# Major cities
curl http://localhost:5000/weather/London,UK
curl http://localhost:5000/weather/New%20York,USA
curl http://localhost:5000/weather/Tokyo,Japan
curl http://localhost:5000/weather/Paris,France
curl http://localhost:5000/weather/Sydney,Australia

# Different formats
curl http://localhost:5000/weather/Berlin,Germany
curl "http://localhost:5000/weather/Berlin?unit=us"
curl "http://localhost:5000/weather/Berlin?format=full"
```

## Troubleshooting Commands

### Check if Flask is installed
```bash
python -c "import flask; print(flask.__version__)"
```

### Check if Redis is installed
```bash
python -c "import redis; print(redis.__version__)"
```

### Check if requests is installed
```bash
python -c "import requests; print(requests.__version__)"
```

### Test Redis connection
```bash
python -c "import redis; r = redis.Redis(); print(r.ping())"
```

### Check API is running
```bash
curl http://localhost:5000/health
```

## Quick Reference

### Start everything
```bash
# Terminal 1: Start Redis (if using Docker)
docker run -d -p 6379:6379 --name redis redis:alpine

# Terminal 2: Start API
python app.py

# Terminal 3: Test API
python test_api.py
```

### Stop everything
```bash
# Stop API: Ctrl+C in the terminal

# Stop Redis (Docker)
docker stop redis
```

### Restart API
```bash
# Stop with Ctrl+C, then:
python app.py
```

## Production Deployment

### Using Gunicorn
```bash
# Install Gunicorn (already in requirements.txt)
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Run with custom timeout
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 app:app

# Run in background
gunicorn -w 4 -b 0.0.0.0:5000 --daemon app:app
```

### Environment for production
```bash
# Edit .env
FLASK_ENV=production
FLASK_DEBUG=False
RATE_LIMIT=1000 per hour
```

## Monitoring Commands

### Watch logs
```bash
# Run the app and watch console output
python app.py

# Or redirect to file
python app.py > app.log 2>&1
```

### Monitor Redis
```bash
# Connect to Redis CLI
docker exec -it redis redis-cli

# Monitor all commands
MONITOR

# Get info
INFO

# Get stats
INFO stats
```

### Check cache hit rate
```bash
curl http://localhost:5000/cache/stats
```

---

**Pro Tip:** Bookmark this file for quick reference!
