# Claude News - Multi-Protocol Information Suite

A hybrid MCP server collection demonstrating mixed local/remote server integration for real-time information aggregation including crypto prices, weather data, and news feeds.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![MCP](https://img.shields.io/badge/MCP-Hybrid-orange)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 🎯 Overview

This project showcases how to combine different MCP transport protocols (SSE remote servers and stdio local servers) to create a comprehensive information aggregation system for Claude Desktop.

### Architecture Pattern
```
Claude Desktop
    ├── SSE Remote → CoinGecko API (Crypto Prices)
    ├── stdio Local → OpenWeather API (Weather Data)  
    ├── stdio Local → News API (Headlines)
    └── stdio Local → Custom Aggregator (Data Processing)
```

## ✨ Features

### Multi-Protocol Integration
- **🌐 SSE Remote Servers** - Real-time crypto price feeds via CoinGecko
- **🖥️ Local stdio Servers** - Weather and news data processing
- **🔄 Mixed Transport** - Demonstrates protocol flexibility
- **📊 Data Aggregation** - Unified information interface

### Information Sources
- **💰 Cryptocurrency Prices** - Real-time market data via CoinGecko SSE
- **🌤️ Weather Information** - Current conditions and forecasts via OpenWeather API
- **📰 News Headlines** - Latest news from multiple sources
- **📈 Market Analysis** - Crypto trends and insights

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│                Claude Desktop                       │
└─────┬─────────┬─────────┬─────────┬─────────────────┘
      │         │         │         │
      │ SSE     │ stdio   │ stdio   │ stdio
      │         │         │         │
┌─────▼───┐ ┌───▼───┐ ┌───▼───┐ ┌───▼────┐
│CoinGecko│ │Weather│ │ News  │ │Aggreg- │
│SSE      │ │Server │ │Server │ │ator    │
│Remote   │ │Local  │ │Local  │ │Local   │
└─────────┘ └───────┘ └───────┘ └────────┘
      │         │         │         │
      │         │         │         │
┌─────▼─────────▼─────────▼─────────▼─────┐
│           External APIs                 │
│  • CoinGecko API                       │
│  • OpenWeather API                     │
│  • News APIs                           │
└───────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Claude Desktop application
- API keys for external services
- Internet connection for remote servers

### 1. Clone and Setup

```bash
# Create project directory
mkdir claude-news && cd claude-news

# Set up Python environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install mcp httpx python-dotenv requests
```

### 2. Configuration Files

**Create `.env` file:**
```bash
# OpenWeather API Key (get from https://openweathermap.org/api)
OPENWEATHER_API_KEY=your_openweather_api_key_here

# News API Key (get from https://newsapi.org)
NEWS_API_KEY=your_news_api_key_here

# Default locations
DEFAULT_CITY=London
DEFAULT_COUNTRY=UK
```

**Create `requirements.txt`:**
```txt
mcp>=1.2.0
httpx>=0.25.0
python-dotenv>=1.0.0
requests>=2.31.0
fastmcp>=0.2.0
```

### 3. Create Server Files

**Weather Server (`weather_server.py`):**
```python
#!/usr/bin/env python3
"""
Weather MCP Server - OpenWeather API Integration
"""
import os
import sys
import logging
from datetime import datetime
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("weather-server")

# Initialize MCP server
mcp = FastMCP("weather")

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5"

@mcp.tool()
async def get_current_weather(city: str = "London", country: str = "UK") -> str:
    """Get current weather conditions for a city."""
    if not API_KEY:
        return "❌ Error: OpenWeather API key not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/weather",
                params={
                    "q": f"{city},{country}",
                    "appid": API_KEY,
                    "units": "metric"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            humidity = data["main"]["humidity"]
            description = data["weather"][0]["description"].title()
            
            return f"""🌤️ Weather in {city}, {country}:
Temperature: {temp}°C (feels like {feels_like}°C)
Conditions: {description}
Humidity: {humidity}%
Updated: {datetime.now().strftime("%H:%M")}"""
            
    except httpx.HTTPStatusError as e:
        return f"❌ Weather API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def get_weather_forecast(city: str = "London", country: str = "UK") -> str:
    """Get 5-day weather forecast for a city."""
    if not API_KEY:
        return "❌ Error: OpenWeather API key not configured"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/forecast",
                params={
                    "q": f"{city},{country}",
                    "appid": API_KEY,
                    "units": "metric"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            forecast_text = f"📅 5-Day Forecast for {city}, {country}:\n\n"
            
            # Group by day and take first forecast per day
            days_shown = 0
            current_date = None
            
            for item in data["list"]:
                if days_shown >= 5:
                    break
                    
                date = datetime.fromtimestamp(item["dt"]).date()
                if date != current_date:
                    current_date = date
                    days_shown += 1
                    
                    temp = item["main"]["temp"]
                    description = item["weather"][0]["description"].title()
                    day_name = date.strftime("%A")
                    
                    forecast_text += f"{day_name}: {temp}°C, {description}\n"
            
            return forecast_text
            
    except httpx.HTTPStatusError as e:
        return f"❌ Weather API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting Weather MCP server...")
    if not API_KEY:
        logger.warning("OPENWEATHER_API_KEY not set")
    mcp.run(transport='stdio')
```

**News Server (`news_server.py`):**
```python
#!/usr/bin/env python3
"""
News MCP Server - News API Integration
"""
import os
import sys
import logging
from datetime import datetime
import httpx
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stderr)
logger = logging.getLogger("news-server")

# Initialize MCP server
mcp = FastMCP("news")

# Configuration
API_KEY = os.getenv("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2"

@mcp.tool()
async def get_top_headlines(country: str = "us", category: str = "", limit: str = "5") -> str:
    """Get top news headlines by country and category."""
    if not API_KEY:
        return "❌ Error: News API key not configured"
    
    try:
        limit_int = int(limit) if limit.strip() else 5
        limit_int = min(limit_int, 20)  # Cap at 20
        
        params = {
            "apiKey": API_KEY,
            "country": country,
            "pageSize": limit_int
        }
        
        if category.strip():
            params["category"] = category
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/top-headlines",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "ok":
                return f"❌ News API Error: {data.get('message', 'Unknown error')}"
            
            articles = data["articles"]
            if not articles:
                return f"📰 No news found for {country}" + (f" in {category}" if category else "")
            
            news_text = f"📰 Top Headlines ({country.upper()}" + (f" - {category.title()}" if category else "") + f"):\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article["title"]
                source = article["source"]["name"]
                published = article["publishedAt"][:10]  # Just the date
                
                news_text += f"{i}. {title}\n"
                news_text += f"   Source: {source} | {published}\n\n"
            
            return news_text
            
    except ValueError:
        return f"❌ Error: Invalid limit value: {limit}"
    except httpx.HTTPStatusError as e:
        return f"❌ News API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

@mcp.tool()
async def search_news(query: str, language: str = "en", limit: str = "5") -> str:
    """Search for news articles by keyword."""
    if not API_KEY:
        return "❌ Error: News API key not configured"
    
    if not query.strip():
        return "❌ Error: Search query is required"
    
    try:
        limit_int = int(limit) if limit.strip() else 5
        limit_int = min(limit_int, 20)  # Cap at 20
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{BASE_URL}/everything",
                params={
                    "apiKey": API_KEY,
                    "q": query,
                    "language": language,
                    "pageSize": limit_int,
                    "sortBy": "publishedAt"
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if data["status"] != "ok":
                return f"❌ News API Error: {data.get('message', 'Unknown error')}"
            
            articles = data["articles"]
            if not articles:
                return f"📰 No news found for query: {query}"
            
            news_text = f"🔍 Search Results for '{query}':\n\n"
            
            for i, article in enumerate(articles, 1):
                title = article["title"]
                source = article["source"]["name"]
                published = article["publishedAt"][:10]
                
                news_text += f"{i}. {title}\n"
                news_text += f"   Source: {source} | {published}\n\n"
            
            return news_text
            
    except ValueError:
        return f"❌ Error: Invalid limit value: {limit}"
    except httpx.HTTPStatusError as e:
        return f"❌ News API Error: {e.response.status_code}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    logger.info("Starting News MCP server...")
    if not API_KEY:
        logger.warning("NEWS_API_KEY not set")
    mcp.run(transport='stdio')
```

### 4. Claude Desktop Configuration

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "coingecko-sse": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-coingecko"]
    },
    "weather": {
      "command": "python",
      "args": ["/path/to/claude-news/weather_server.py"],
      "env": {
        "OPENWEATHER_API_KEY": "your_api_key_here"
      }
    },
    "news": {
      "command": "python", 
      "args": ["/path/to/claude-news/news_server.py"],
      "env": {
        "NEWS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

## 💻 Usage Examples

### Information Queries

**Crypto Market Data:**
```
"What's the current price of Bitcoin and Ethereum?"
"Show me the top 10 cryptocurrencies by market cap"
"How has Solana performed in the last 24 hours?"
```

**Weather Information:**
```
"What's the current weather in London?"
"Give me a 5-day forecast for New York"
"How's the weather in Tokyo, Japan?"
```

**News Headlines:**
```
"Show me the top 5 news headlines from the US"
"Get technology news from the UK"
"Search for news about artificial intelligence"
```

### Combined Workflows

**Morning Briefing:**
```
"Give me a morning briefing: 
1. Current weather in my city
2. Top 3 news headlines
3. Bitcoin and Ethereum prices
4. Any major crypto market movements"
```

**Market Analysis:**
```
"Create a market summary:
1. Top 5 crypto prices and 24h changes
2. Search for news about 'cryptocurrency regulation'
3. Weather in major financial centers (NYC, London, Tokyo)"
```

**Travel Planning:**
```
"I'm traveling to Paris tomorrow:
1. Get weather forecast for Paris, France
2. Search for news about 'France travel'
3. Current EUR/USD rate (if available via crypto data)"
```

## 🔧 Configuration Details

### API Keys Setup

**OpenWeather API:**
1. Sign up at https://openweathermap.org/api
2. Get free API key (1000 calls/day)
3. Add to `.env` file

**News API:**
1. Sign up at https://newsapi.org
2. Get free API key (1000 requests/day)
3. Add to `.env` file

**CoinGecko (SSE):**
- No API key required for basic usage
- Uses public SSE endpoint
- Rate limited but sufficient for personal use

### Transport Protocols

| Server | Protocol | Reason |
|--------|----------|---------|
| CoinGecko | SSE Remote | Real-time price updates, maintained by community |
| Weather | stdio Local | Custom API integration, local processing |
| News | stdio Local | Custom filtering and formatting |

### Environment Variables

```bash
# Required for weather functionality
OPENWEATHER_API_KEY=your_openweather_api_key

# Required for news functionality  
NEWS_API_KEY=your_news_api_key

# Optional customization
DEFAULT_CITY=London
DEFAULT_COUNTRY=UK
DEFAULT_NEWS_COUNTRY=us
```

## 📊 Project Structure

```
claude-news/
├── README.md                   # This file
├── .env                        # Environment variables (create from template)
├── .env.example               # Environment template
├── requirements.txt           # Python dependencies
├── weather_server.py          # Weather MCP server
├── news_server.py            # News MCP server
├── docs/
│   ├── api-setup-guide.md    # API key setup instructions
│   ├── transport-protocols.md # MCP transport explanation
│   └── troubleshooting.md    # Common issues
├── examples/
│   ├── claude-config.json    # Complete Claude Desktop config
│   ├── workflow-examples.md  # Usage examples and workflows
│   └── demo-queries.txt      # Sample queries for testing
└── scripts/
    ├── setup.sh             # Automated setup script
    ├── test-servers.sh      # Server testing script
    └── update-apis.sh       # API key update script
```

## 🧪 Testing

### Test Individual Servers

**Weather Server:**
```bash
# Activate virtual environment
source venv/bin/activate

# Test weather server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python weather_server.py
```

**News Server:**
```bash
# Test news server
echo '{"jsonrpc":"2.0","method":"tools/list","id":1}' | python news_server.py
```

### Test in Claude Desktop

**Basic Functionality:**
```
"List all available tools"
"What weather tools do you have?"
"Show me news capabilities"
"What crypto data can you access?"
```

**Integration Test:**
```
"Test all information sources:
1. Get weather for London
2. Get top 3 US news headlines  
3. Get Bitcoin price
4. Confirm all systems are working"
```

## 🔍 Troubleshooting

### Common Issues

**API Key Errors:**
```bash
# Check environment variables
echo $OPENWEATHER_API_KEY
echo $NEWS_API_KEY

# Test API keys directly
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY"
```

**Server Not Starting:**
```bash
# Check Python environment
which python
python --version

# Test MCP imports
python -c "from mcp.server.fastmcp import FastMCP; print('MCP OK')"

# Check dependencies
pip list | grep -E "(mcp|httpx|dotenv)"
```

**Claude Desktop Issues:**
```bash
# Validate JSON configuration
python -m json.tool ~/Library/Application\ Support/Claude/claude_desktop_config.json

# Check file paths
ls -la /path/to/claude-news/weather_server.py
ls -la /path/to/claude-news/news_server.py
```

### Debug Mode

**Enable Verbose Logging:**
```python
# Add to server files
logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
```

**Test API Connections:**
```bash
# Create test script
cat > test_apis.py << 'EOF'
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_apis():
    # Test OpenWeather
    weather_key = os.getenv("OPENWEATHER_API_KEY")
    if weather_key:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={weather_key}"
            )
            print(f"Weather API: {response.status_code}")
    
    # Test News API
    news_key = os.getenv("NEWS_API_KEY")
    if news_key:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_key}"
            )
            print(f"News API: {response.status_code}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_apis())
EOF

python test_apis.py
```

## 🚧 Future Enhancements

### Planned Features
- [ ] **Additional Data Sources** - Stock prices, forex rates, social media trends
- [ ] **Caching Layer** - Redis integration for API response caching
- [ ] **WebSocket Support** - Real-time data streaming
- [ ] **Custom Aggregations** - User-defined data combinations
- [ ] **Alert System** - Notifications for price/weather/news thresholds

### Integration Opportunities
- [ ] **Slack Bot** - Information delivery to Slack channels
- [ ] **Discord Integration** - Community information sharing
- [ ] **Mobile App** - React Native or Flutter client
- [ ] **Web Dashboard** - Real-time information display
- [ ] **Voice Assistant** - Alexa/Google Home integration

## 🤝 Contributing

Contributions welcome! Areas for improvement:

### New Data Sources
- Financial APIs (Alpha Vantage, Yahoo Finance)
- Social media APIs (Twitter, Reddit)
- Government data APIs
- Sports and entertainment APIs

### Protocol Enhancements
- WebSocket transport implementation
- HTTP polling servers
- GraphQL integration
- gRPC support

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/claude-news
cd claude-news

# Set up development environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Test servers
./scripts/test-servers.sh
```

## 📄 License

MIT License - See [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- **[CoinGecko](https://www.coingecko.com)** - Cryptocurrency data API
- **[OpenWeather](https://openweathermap.org)** - Weather data API  
- **[NewsAPI](https://newsapi.org)** - News aggregation service
- **[Anthropic](https://www.anthropic.com)** - MCP specification and Claude Desktop
- **MCP Community** - SSE server implementations and examples

---

*This project demonstrates the flexibility of MCP transport protocols and how to integrate multiple information sources for comprehensive AI assistance.*
