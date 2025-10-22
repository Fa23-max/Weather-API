# Weather API - Project Overview

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Features](#features)
- [Documentation](#documentation)
- [Technology Stack](#technology-stack)
- [Key Concepts](#key-concepts)

## 🚀 Quick Start

**Get started in 3 commands:**

```bash
python setup_env.py          # Create .env file
pip install -r requirements.txt   # Install dependencies
python app.py                # Start the API
```

Then test it:
```bash
python test_api.py
```

**Full guide:** See [QUICKSTART.md](QUICKSTART.md)

## 📁 Project Structure

```
Weather Api/
│
├── 📄 Core Application Files
│   ├── app.py                    # Main Flask application & routes
│   ├── config.py                 # Configuration management
│   ├── cache.py                  # Redis cache implementation
│   └── weather_service.py        # Weather API integration
│
├── 📄 Configuration Files
│   ├── .env.example              # Example environment variables
│   ├── .gitignore                # Git ignore rules
│   └── requirements.txt          # Python dependencies
│
├── 📄 Testing & Examples
│   ├── test_api.py               # Comprehensive API tests
│   ├── example_usage.py          # Usage examples
│   └── setup_env.py              # Environment setup script
│
└── 📄 Documentation
    ├── README.md                 # Complete documentation
    ├── QUICKSTART.md             # Quick start guide
    ├── SETUP.md                  # Detailed setup instructions
    ├── ARCHITECTURE.md           # System architecture
    ├── COMMANDS.md               # Command reference
    └── PROJECT_OVERVIEW.md       # This file
```

## ✨ Features

### Core Features
- ✅ **Real-time Weather Data** - Fetches from Visual Crossing API
- ✅ **Smart Caching** - Redis-based caching with auto-expiration
- ✅ **Rate Limiting** - Prevents abuse (100 req/hour default)
- ✅ **Multiple Units** - Metric, US, and UK unit systems
- ✅ **Error Handling** - Comprehensive error handling
- ✅ **Logging** - Detailed logging for debugging

### Advanced Features
- ✅ **Graceful Degradation** - Works without Redis
- ✅ **Cache Statistics** - Monitor cache performance
- ✅ **Health Checks** - API health monitoring
- ✅ **Environment Config** - Secure configuration via .env
- ✅ **Production Ready** - Gunicorn support

## 📚 Documentation

### For Getting Started
1. **[QUICKSTART.md](QUICKSTART.md)** - Get running in 3 minutes
2. **[SETUP.md](SETUP.md)** - Detailed setup instructions
3. **[README.md](README.md)** - Complete API documentation

### For Development
4. **[ARCHITECTURE.md](ARCHITECTURE.md)** - System design & architecture
5. **[COMMANDS.md](COMMANDS.md)** - Command reference
6. **[example_usage.py](example_usage.py)** - Code examples

### Quick Links
- **Need help?** → Start with [QUICKSTART.md](QUICKSTART.md)
- **Want details?** → Read [README.md](README.md)
- **Understanding design?** → See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Looking for commands?** → Check [COMMANDS.md](COMMANDS.md)

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Web Framework** | Flask | 3.0.0 | HTTP server & routing |
| **Cache** | Redis | 5.0.1 | In-memory data store |
| **HTTP Client** | Requests | 2.31.0 | External API calls |
| **Rate Limiting** | Flask-Limiter | 3.5.0 | Request throttling |
| **Configuration** | python-dotenv | 1.0.0 | Environment variables |
| **WSGI Server** | Gunicorn | 21.2.0 | Production deployment |
| **Weather API** | Visual Crossing | Free Tier | Weather data source |

## 🎯 Key Concepts

### 1. API Integration
This project demonstrates how to:
- Integrate with 3rd party APIs (Visual Crossing)
- Handle API errors and timeouts
- Parse and format API responses
- Manage API keys securely

**Learn more:** [weather_service.py](weather_service.py)

### 2. Caching Strategy
Implements intelligent caching:
- Cache key design: `weather:{location}:{unit}`
- Automatic expiration (12 hours default)
- Cache hit/miss tracking
- Graceful degradation without Redis

**Learn more:** [cache.py](cache.py)

### 3. Rate Limiting
Prevents API abuse:
- Per-IP rate limiting
- Configurable limits
- Uses Redis for distributed limiting
- Returns 429 when exceeded

**Learn more:** [app.py](app.py) - Rate limiter setup

### 4. Environment Configuration
Secure configuration management:
- API keys in .env (not in code)
- Different configs for dev/prod
- Validation of required settings
- Easy to customize

**Learn more:** [config.py](config.py)

### 5. Error Handling
Comprehensive error handling:
- Invalid input validation
- API error handling
- Network timeout handling
- Graceful degradation

**Learn more:** [app.py](app.py) - Error handlers

## 🔄 Request Flow

```
1. Client Request
   ↓
2. Rate Limiter (Check limit)
   ↓
3. Cache Check (Redis)
   ↓
4a. Cache HIT → Return cached data (fast!)
   ↓
4b. Cache MISS → Fetch from Visual Crossing API
   ↓
5. Format & Cache Response
   ↓
6. Return to Client
```

**Detailed flow:** See [ARCHITECTURE.md](ARCHITECTURE.md)

## 📊 Performance

### Without Cache
- Response time: ~500-1000ms
- Limited by external API
- Subject to API rate limits

### With Cache (Hit)
- Response time: ~10-50ms
- 50-100x faster
- No external API calls

### Cache Hit Rate
- Expected: 80-90% for popular locations
- Configurable TTL (default: 12 hours)

## 🔐 Security

### API Key Protection
- Stored in `.env` file (gitignored)
- Never exposed in responses
- Server-side only

### Rate Limiting
- Per-IP address
- Prevents abuse
- Configurable limits

### Input Validation
- Location parameter validated
- Unit parameter validated
- Error messages sanitized

## 🧪 Testing

### Automated Tests
```bash
python test_api.py
```

Tests include:
- API home endpoint
- Health check
- Weather requests (fresh & cached)
- Different unit systems
- Invalid locations
- Cache statistics

### Manual Testing
```bash
# Basic test
curl http://localhost:5000/weather/London,UK

# Test caching (run twice)
curl http://localhost:5000/weather/Tokyo
curl http://localhost:5000/weather/Tokyo

# Check cache stats
curl http://localhost:5000/cache/stats
```

### Example Usage
```bash
python example_usage.py
```

Demonstrates:
- Simple weather requests
- Temperature-only queries
- Forecast retrieval
- Different unit systems
- Error handling
- Batch requests

## 🚀 Deployment

### Development
```bash
python app.py
```

### Production
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Environment Variables
```env
# Development
FLASK_ENV=development
FLASK_DEBUG=True

# Production
FLASK_ENV=production
FLASK_DEBUG=False
RATE_LIMIT=1000 per hour
```

## 📈 Monitoring

### Health Check
```bash
curl http://localhost:5000/health
```

### Cache Statistics
```bash
curl http://localhost:5000/cache/stats
```

Returns:
- Cache enabled status
- Total keys
- Cache hits
- Cache misses

### Logs
All operations are logged:
- Request received
- Cache hit/miss
- API calls
- Errors

## 🎓 Learning Outcomes

By studying this project, you'll learn:

1. **API Development**
   - RESTful API design
   - Route handling
   - Request/response formatting

2. **3rd Party Integration**
   - External API calls
   - Error handling
   - Data transformation

3. **Caching**
   - Cache key design
   - TTL management
   - Cache invalidation

4. **Rate Limiting**
   - Request throttling
   - Distributed rate limiting
   - Abuse prevention

5. **Configuration Management**
   - Environment variables
   - Secure credential storage
   - Multi-environment config

6. **Error Handling**
   - Validation
   - Exception handling
   - Graceful degradation

7. **Production Practices**
   - Logging
   - Monitoring
   - Health checks
   - Documentation

## 🔧 Customization

### Change Cache Duration
Edit `.env`:
```env
CACHE_EXPIRATION=21600  # 6 hours in seconds
```

### Change Rate Limit
Edit `.env`:
```env
RATE_LIMIT=200 per hour
```

### Change Port
Edit `.env`:
```env
PORT=8000
```

### Use Different Weather API
Edit `weather_service.py` and update the API endpoint and request format.

## 🐛 Troubleshooting

### Common Issues

**"WEATHER_API_KEY is required"**
```bash
python setup_env.py
```

**"Redis connection failed"**
- Redis is optional, API will still work
- To enable: Install and start Redis

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Port already in use"**
- Change port in `.env`
- Or kill process on port 5000

**Full troubleshooting:** See [README.md](README.md#troubleshooting)

## 📞 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/weather/<location>` | Get weather data |
| GET | `/cache/stats` | Cache statistics |
| DELETE | `/cache/clear` | Clear all cache |

**Full API docs:** See [README.md](README.md#api-endpoints)

## 🎯 Next Steps

1. ✅ **Get it running** → [QUICKSTART.md](QUICKSTART.md)
2. 📖 **Read the docs** → [README.md](README.md)
3. 🧪 **Run tests** → `python test_api.py`
4. 💻 **Try examples** → `python example_usage.py`
5. 🏗️ **Understand design** → [ARCHITECTURE.md](ARCHITECTURE.md)
6. 🚀 **Deploy it** → See [README.md](README.md#production-deployment)

## 🌟 Features to Add (Ideas)

Want to extend this project? Consider adding:

1. **Database Integration** - Store historical weather data
2. **User Authentication** - API keys for users
3. **Webhooks** - Alert on weather changes
4. **GraphQL API** - More flexible queries
5. **WebSocket** - Real-time updates
6. **Analytics Dashboard** - Visualize usage
7. **Multiple Weather APIs** - Fallback sources
8. **Batch Endpoints** - Get multiple locations at once

## 📝 Code Quality

### Best Practices Used
- ✅ Modular design (separation of concerns)
- ✅ Environment-based configuration
- ✅ Comprehensive error handling
- ✅ Detailed logging
- ✅ Input validation
- ✅ Security best practices
- ✅ Extensive documentation
- ✅ Example code provided
- ✅ Production-ready setup

### Code Structure
- **app.py** - Routes and application logic
- **config.py** - Configuration management
- **cache.py** - Cache abstraction layer
- **weather_service.py** - External API integration

Each module has a single responsibility and is independently testable.

## 🤝 Contributing

This is a learning project. Feel free to:
- Modify and experiment
- Add new features
- Improve documentation
- Share with others

## 📄 License

Open source - Free for educational purposes

---

## 🎉 You're Ready!

You now have a complete, production-ready Weather API with:
- ✅ Real-time weather data
- ✅ Intelligent caching
- ✅ Rate limiting
- ✅ Comprehensive documentation
- ✅ Example code
- ✅ Testing suite

**Start here:** [QUICKSTART.md](QUICKSTART.md)

**Questions?** Check the documentation files listed above!

---

**Happy coding! 🚀**
