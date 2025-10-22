# Quick Setup Guide

## Step 1: Install Dependencies

Open a terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
copy .env.example .env
```

Then edit the `.env` file and add your Visual Crossing API key:

```env
WEATHER_API_KEY=76ESP89QU2Q5T4HVLMGQVRB8J
```

**Important:** Replace with your actual API key if different.

## Step 3: Install Redis (Optional but Recommended)

### Option A: Using Docker (Easiest)
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

### Option B: Windows Installation
1. Download Redis from: https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

### Option C: Skip Redis
The API will work without Redis, but caching will be disabled. Just start the API in Step 4.

## Step 4: Start the API

```bash
python app.py
```

You should see:
```
Starting Weather API on port 5000
Debug mode: True
Cache enabled: True
```

## Step 5: Test the API

Open a new terminal and run:

```bash
python test_api.py
```

Or test manually with curl:

```bash
curl http://localhost:5000/weather/London,UK
```

Or open in your browser:
```
http://localhost:5000/
```

## Troubleshooting

### "WEATHER_API_KEY is required"
- Make sure you created the `.env` file
- Make sure `WEATHER_API_KEY` is set in the `.env` file

### "Redis connection failed"
- Redis is optional - the API will still work
- To enable caching, install and start Redis (see Step 3)

### "Module not found"
- Make sure you installed dependencies: `pip install -r requirements.txt`
- Make sure you're in the correct directory

## Next Steps

- Read the full documentation in `README.md`
- Customize configuration in `.env`
- Deploy to production with Gunicorn
