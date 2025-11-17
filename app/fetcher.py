import httpx
from .config import settings
from typing import Tuple, Dict, Any

async def fetch_from_openweather(city: str) -> Tuple[bool, Dict]:
    
    if settings.openweather_api_key:
        params = {"q": city, "appid": settings.openweather_api_key, "units": "metric"}
        async with httpx.AsyncClient(timeout=10.0) as client:
            r = await client.get(settings.openweather_base_url, params=params)
            if r.status_code == 200:
                return True, r.json()
            else:
                # handle city not found (404) errors
                return False, {"status_code": r.status_code, "detail": r.text}
    else:
        async with httpx.AsyncClient(timeout=10.0) as client:
            geocode = await client.get("https://geocoding-api.open-meteo.com/v1/search", params={"name": city, "count":1})
            if geocode.status_code != 200:
                return False, {"status_code": geocode.status_code, "detail": geocode.text}
            data = geocode.json()
            results = data.get("results")
            if not results:
                return False, {"status_code": 404, "detail": "city not found"}
            lat = results[0]["latitude"]
            lon = results[0]["longitude"]
            weather = await client.get("https://api.open-meteo.com/v1/forecast", params={
                "latitude": lat, "longitude": lon, "current_weather": True
            })
            if weather.status_code == 200:
                return True, {
                    "open_meteo": weather.json(),
                    "geocoding": results[0]
                }
            else:
                return False, {"status_code": weather.status_code, "detail": weather.text}