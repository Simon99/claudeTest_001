# claudeTest_001
used for claude github task test

## Taiwan Weather Forecast Feature

This repository includes an automated weather forecast feature for Taiwan's 5 major cities.

### Features

- Automatic daily updates via GitHub Actions
- 7-day weather forecast for:
  - 台北市 (Taipei)
  - 新北市 (New Taipei)
  - 台中市 (Taichung)
  - 台南市 (Tainan)
  - 高雄市 (Kaohsiung)
- Beautiful HTML output with responsive design
- Fallback data when API is unavailable

### Setup

1. Add your OpenWeatherMap API key as a GitHub secret:
   - Go to Settings → Secrets → Actions
   - Add a new secret named `OPENWEATHER_API_KEY`
   - Get your API key from [OpenWeatherMap](https://openweathermap.org/api)

### How it works

The GitHub Action runs daily at 2:00 PM Taiwan time (6:00 AM UTC) and:
1. Fetches weather data from OpenWeatherMap API
2. Generates an HTML file with the forecast
3. Commits and pushes the updated file if there are changes

You can also trigger the workflow manually from the Actions tab.
