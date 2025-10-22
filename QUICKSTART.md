# Quick Start Guide

Get your Weather API up and running in 3 minutes!

## 🚀 Quick Setup (3 steps)

### 1️⃣ Create Environment File
```bash
python setup_env.py
```
This will create a `.env` file with your API key already configured.

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Start the API
```bash
python app.py
```

**That's it!** Your API is now running at `http://localhost:5000`

## 🧪 Test It

### Option A: Run the test script
```bash
python test_api.py
```

### Option B: Try it in your browser
Open: http://localhost:5000/weather/London,UK

### Option C: Use curl
```bash
curl http://localhost:5000/weather/London,UK
```

## 📚 Example Usage

See how to use the API in your own code:
```bash
python example_usage.py
```

## 🔧 Optional: Redis Caching

The API works without Redis, but for better performance:

**Using Docker (easiest):**
```bash
docker run -d -p 6379:6379 --name redis redis:alpine
```

Then restart the API.

## 📖 Full Documentation

- **SETUP.md** - Detailed setup instructions
- **README.md** - Complete API documentation
- **example_usage.py** - Code examples

## 🆘 Troubleshooting

**"WEATHER_API_KEY is required"**
- Run: `python setup_env.py`

**"Module not found"**
- Run: `pip install -r requirements.txt`

**"Connection refused"**
- Make sure the API is running: `python app.py`

## 🎯 Next Steps

1. ✅ API is running
2. ✅ Test it works
3. 📖 Read the full documentation in README.md
4. 🔧 Customize settings in .env
5. 🚀 Build something awesome!

## 📝 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | API information |
| `GET /weather/<location>` | Get weather data |
| `GET /health` | Health check |
| `GET /cache/stats` | Cache statistics |
| `DELETE /cache/clear` | Clear cache |

## 💡 Tips

- Weather data is cached for 12 hours by default
- Rate limit: 100 requests per hour per IP
- Supports metric, US, and UK units
- Works with or without Redis

---

**Need help?** Check the full documentation in README.md
