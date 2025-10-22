# Weather API Architecture

## System Overview

```
┌─────────────┐
│   Client    │
│ (Browser/   │
│  App/Curl)  │
└──────┬──────┘
       │
       │ HTTP Request
       │ GET /weather/London,UK
       ▼
┌─────────────────────────────────────────────────────────┐
│                    Flask Application                     │
│                        (app.py)                          │
├─────────────────────────────────────────────────────────┤
│                                                           │
│  ┌──────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ Rate Limiter │───▶│   Routes     │───▶│  Config   │ │
│  │ (Flask-      │    │              │    │ (.env)    │ │
│  │  Limiter)    │    │ /weather/:loc│    └───────────┘ │
│  └──────────────┘    │ /health      │                   │
│                      │ /cache/stats │                   │
│                      └──────┬───────┘                   │
│                             │                            │
│                             ▼                            │
│                      ┌──────────────┐                   │
│                      │ Cache Check  │                   │
│                      │ (cache.py)   │                   │
│                      └──────┬───────┘                   │
│                             │                            │
│                    ┌────────┴────────┐                  │
│                    │                 │                  │
│              Cache HIT          Cache MISS              │
│                    │                 │                  │
│                    ▼                 ▼                  │
│            ┌──────────────┐  ┌──────────────┐          │
│            │ Return Cached│  │Weather Service│          │
│            │     Data     │  │(weather_      │          │
│            └──────────────┘  │ service.py)  │          │
│                              └──────┬───────┘          │
│                                     │                   │
└─────────────────────────────────────┼───────────────────┘
                                      │
                                      │ HTTP Request
                                      ▼
                              ┌──────────────┐
                              │Visual Crossing│
                              │  Weather API  │
                              └──────┬───────┘
                                     │
                                     │ JSON Response
                                     ▼
                              ┌──────────────┐
                              │ Format Data  │
                              │ Cache Result │
                              │ Return to    │
                              │   Client     │
                              └──────────────┘

┌─────────────────────────────────────────────────────────┐
│                    Redis Cache                           │
│                                                           │
│  Key: weather:london,uk:metric                          │
│  Value: { "location": "London", "current": {...} }      │
│  TTL: 43200 seconds (12 hours)                          │
│                                                           │
│  Auto-expires old data                                   │
└─────────────────────────────────────────────────────────┘
```

## Component Details

### 1. **Flask Application (app.py)**
- Main entry point
- Handles HTTP requests and responses
- Coordinates between components
- Implements error handling

### 2. **Rate Limiter (Flask-Limiter)**
- Prevents API abuse
- Default: 100 requests per hour per IP
- Uses Redis for distributed rate limiting
- Falls back to in-memory if Redis unavailable

### 3. **Configuration (config.py)**
- Loads environment variables from `.env`
- Validates required settings
- Provides centralized configuration

### 4. **Cache Manager (cache.py)**
- Manages Redis connections
- Implements get/set/delete operations
- Handles cache expiration (TTL)
- Gracefully degrades if Redis unavailable

### 5. **Weather Service (weather_service.py)**
- Communicates with Visual Crossing API
- Handles API errors and timeouts
- Formats weather data
- Supports multiple unit systems

### 6. **Redis Cache**
- In-memory data store
- Stores weather data with automatic expiration
- Key format: `weather:{location}:{unit}`
- Default TTL: 12 hours (43200 seconds)

## Request Flow

### First Request (Cache Miss)
1. Client sends request: `GET /weather/London,UK`
2. Rate limiter checks request limit
3. App checks Redis cache for key: `weather:london,uk:metric`
4. Cache miss - no data found
5. Weather service fetches from Visual Crossing API
6. Data is formatted and cached in Redis with 12-hour TTL
7. Response returned to client with `"cached": false`

### Subsequent Request (Cache Hit)
1. Client sends request: `GET /weather/London,UK`
2. Rate limiter checks request limit
3. App checks Redis cache for key: `weather:london,uk:metric`
4. Cache hit - data found and not expired
5. Cached data returned immediately
6. Response returned to client with `"cached": true`

### After 12 Hours
- Redis automatically removes expired key
- Next request will be a cache miss
- Fresh data fetched from API
- Cycle repeats

## Data Flow

```
Request → Rate Limit → Cache Check → API Call → Format → Cache → Response
                           ↓                                ↑
                      [If cached] ─────────────────────────┘
```

## Error Handling

### API Errors
- **400 Bad Request**: Invalid location or parameters
- **401 Unauthorized**: Invalid API key
- **429 Too Many Requests**: Rate limit exceeded
- **503 Service Unavailable**: Weather API down
- **504 Gateway Timeout**: Weather API timeout

### Graceful Degradation
- **Redis unavailable**: API continues without caching
- **Weather API down**: Returns appropriate error message
- **Invalid input**: Returns validation error

## Caching Strategy

### Why Cache?
- Reduces API calls to Visual Crossing
- Improves response time (cached: ~10ms vs API: ~500ms)
- Reduces costs (Visual Crossing has rate limits)
- Weather data doesn't change frequently

### Cache Key Design
```
weather:{location}:{unit}
```

Examples:
- `weather:london,uk:metric`
- `weather:new york:us`
- `weather:paris:metric`

### Cache Expiration
- Default: 12 hours (43200 seconds)
- Configurable via `CACHE_EXPIRATION` in `.env`
- Automatic cleanup by Redis (no manual intervention needed)

### Cache Invalidation
- Automatic: Redis TTL expires
- Manual: `DELETE /cache/clear` endpoint
- Per-key: Delete specific location cache

## Performance Characteristics

### Without Cache
- Response time: ~500-1000ms
- Limited by Visual Crossing API rate limits
- Each request hits external API

### With Cache (Hit)
- Response time: ~10-50ms (50-100x faster)
- No external API calls
- Scales to handle more requests

### Cache Hit Rate
- Expected: 80-90% for popular locations
- Depends on: request patterns, cache TTL, location diversity

## Security Considerations

### API Key Protection
- Stored in `.env` file (not in git)
- Never exposed in responses
- Server-side only

### Rate Limiting
- Prevents abuse
- Per-IP address
- Configurable limits

### Input Validation
- Location parameter validated
- Unit parameter validated
- Error messages don't leak sensitive info

## Scalability

### Horizontal Scaling
- Multiple API instances can share Redis cache
- Rate limiting works across instances
- Stateless design (no session storage)

### Vertical Scaling
- Redis can handle millions of keys
- Flask can handle thousands of requests/second
- Bottleneck is usually the external API

## Monitoring

### Available Metrics
- Cache hit/miss ratio: `GET /cache/stats`
- Total cached keys: `GET /cache/stats`
- API health: `GET /health`
- Rate limit status: Response headers

### Logging
- All requests logged
- Cache operations logged
- API errors logged
- Format: timestamp, level, message

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Web Framework | Flask 3.0 | HTTP server and routing |
| Cache | Redis 5.0 | In-memory data store |
| HTTP Client | Requests 2.31 | External API calls |
| Rate Limiting | Flask-Limiter 3.5 | Request throttling |
| Config | python-dotenv 1.0 | Environment variables |
| WSGI Server | Gunicorn 21.2 | Production deployment |

## Design Decisions

### Why Flask?
- Lightweight and simple
- Excellent for APIs
- Large ecosystem
- Easy to learn and maintain

### Why Redis?
- Fast (in-memory)
- Built-in TTL support
- Widely used and reliable
- Easy to deploy

### Why Visual Crossing?
- Free tier available
- Good documentation
- Reliable service
- Comprehensive weather data

### Why 12-hour cache?
- Weather changes gradually
- Balance between freshness and performance
- Reduces API costs
- Configurable if needed

## Future Enhancements

### Potential Improvements
1. **Database**: Store historical weather data
2. **Analytics**: Track popular locations
3. **Webhooks**: Alert on weather changes
4. **Batch API**: Get weather for multiple locations
5. **GraphQL**: More flexible queries
6. **WebSocket**: Real-time updates
7. **Authentication**: User accounts and API keys
8. **Metrics**: Prometheus/Grafana integration
