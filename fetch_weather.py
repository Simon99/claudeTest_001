#!/usr/bin/env python3
import os
import json
import requests
from datetime import datetime, timedelta
from typing import Dict, List

# Taiwan's 5 major cities with their coordinates
CITIES = {
    "台北市": {"lat": 25.0330, "lon": 121.5654},
    "新北市": {"lat": 25.0170, "lon": 121.4628},
    "台中市": {"lat": 24.1477, "lon": 120.6736},
    "台南市": {"lat": 22.9998, "lon": 120.2269},
    "高雄市": {"lat": 22.6273, "lon": 120.3014}
}

def fetch_weather_data(api_key: str) -> Dict[str, List[Dict]]:
    """Fetch weather forecast data for all cities"""
    weather_data = {}
    
    for city_name, coords in CITIES.items():
        try:
            # Using OpenWeatherMap One Call API for 7-day forecast
            url = f"https://api.openweathermap.org/data/2.5/onecall"
            params = {
                "lat": coords["lat"],
                "lon": coords["lon"],
                "appid": api_key,
                "units": "metric",
                "lang": "zh_tw",
                "exclude": "minutely,hourly,alerts"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            daily_forecast = []
            
            for day in data["daily"][:7]:  # Get 7 days
                forecast = {
                    "date": datetime.fromtimestamp(day["dt"]),
                    "temp_min": round(day["temp"]["min"]),
                    "temp_max": round(day["temp"]["max"]),
                    "weather": day["weather"][0]["description"],
                    "icon": get_weather_emoji(day["weather"][0]["main"])
                }
                daily_forecast.append(forecast)
            
            weather_data[city_name] = daily_forecast
            
        except Exception as e:
            print(f"Error fetching data for {city_name}: {e}")
            # Use fallback data if API fails
            weather_data[city_name] = generate_fallback_data()
    
    return weather_data

def get_weather_emoji(weather_main: str) -> str:
    """Convert weather condition to emoji"""
    weather_emojis = {
        "Clear": "☀️",
        "Clouds": "☁️",
        "Rain": "🌧️",
        "Drizzle": "🌦️",
        "Thunderstorm": "⛈️",
        "Snow": "❄️",
        "Mist": "🌫️",
        "Fog": "🌫️"
    }
    return weather_emojis.get(weather_main, "🌤️")

def generate_fallback_data() -> List[Dict]:
    """Generate fallback weather data if API fails"""
    fallback_data = []
    base_date = datetime.now()
    
    for i in range(7):
        date = base_date + timedelta(days=i)
        fallback_data.append({
            "date": date,
            "temp_min": 16 + i,
            "temp_max": 24 + i,
            "weather": "晴朗",
            "icon": "☀️"
        })
    
    return fallback_data

def generate_html(weather_data: Dict[str, List[Dict]]) -> str:
    """Generate HTML content with weather data"""
    
    def format_date(date: datetime) -> str:
        weekdays = ["一", "二", "三", "四", "五", "六", "日"]
        return f"{date.month}月{date.day}日 ({weekdays[date.weekday()]})"
    
    cities_html = ""
    for city_name, forecasts in weather_data.items():
        days_html = ""
        for forecast in forecasts:
            days_html += f"""
                <div class="weather-day">
                    <span class="date">{format_date(forecast['date'])}</span>
                    <div class="weather-info">
                        <span class="weather-icon">{forecast['icon']}</span>
                        <span class="temp">{forecast['temp_min']}°C - {forecast['temp_max']}°C</span>
                        <span class="description">{forecast['weather']}</span>
                    </div>
                </div>"""
        
        cities_html += f"""
            <div class="city-card">
                <div class="city-name">{city_name}</div>
                {days_html}
            </div>"""
    
    html_template = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>台灣五大都市未來一週天氣預報</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Microsoft JhengHei', sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f0f2f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            text-align: center;
            color: #1a365d;
            margin-bottom: 30px;
        }}
        .cities-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .city-card {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .city-name {{
            font-size: 24px;
            font-weight: bold;
            color: #2c5282;
            margin-bottom: 15px;
        }}
        .weather-day {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #e2e8f0;
        }}
        .weather-day:last-child {{
            border-bottom: none;
        }}
        .date {{
            font-weight: 600;
            color: #4a5568;
        }}
        .weather-info {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .weather-icon {{
            font-size: 24px;
        }}
        .temp {{
            font-weight: bold;
            color: #2b6cb0;
        }}
        .description {{
            color: #718096;
        }}
        .update-time {{
            text-align: center;
            margin-top: 30px;
            color: #718096;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>台灣五大都市未來一週天氣預報</h1>
        
        <div class="cities-grid">
            {cities_html}
        </div>

        <div class="update-time">
            更新時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M')}
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def main():
    # Get API key from environment variable
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    
    if api_key:
        print("Fetching weather data from OpenWeatherMap API...")
        weather_data = fetch_weather_data(api_key)
    else:
        print("No API key found, using fallback data...")
        weather_data = {city: generate_fallback_data() for city in CITIES}
    
    # Generate HTML
    html_content = generate_html(weather_data)
    
    # Write to file
    with open('taiwan-weather-forecast.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("Weather forecast HTML file generated successfully!")

if __name__ == "__main__":
    main()