from fastapi import FastAPI, HTTPException, Query, Request, status
import uvicorn
from .fetcher import fetch_from_openweather
from .storage import save_weather_response
from .logger_db import log_event
from .cache import get_cached, set_cache
from .config import settings
from .schemas import WeatherResponse
from .rate_limiter import allow_request
import datetime
import asyncio

app = FastAPI(title="Weather API")

@app.on_event("startup")
async def startup():
    try:
        await log_event("__init__", datetime.datetime.utcnow().isoformat(), "init")
    except Exception:
        pass

def _get_client_id(request: Request) -> str:
    ip = request.client.host if request.client else "unknown"
    return ip

@app.get("/weather", response_model=WeatherResponse)
async def weather(request: Request, city: str = Query(..., min_length=1)):
    client = _get_client_id(request)
    allowed = await allow_request(client)
    if not allowed:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")

    cached = await get_cached(city, settings.cache_ttl_seconds)
    if cached:
        return WeatherResponse(source="cache", data=cached["payload"], cached=True, saved_file=cached["saved_file"])

    success, payload = await fetch_from_openweather(city)
    if not success:
        code = payload.get("status_code", 500)
        detail = payload.get("detail", "external API error")
        if code == 404:
            raise HTTPException(status_code=404, detail=f"City '{city}' not found")
        raise HTTPException(status_code=502, detail=f"Weather provider error: {detail}")

    filepath, filename = save_weather_response(city, payload)
    ts = datetime.datetime.utcnow().isoformat()
    asyncio.create_task(log_event(city, ts, filepath))
    await set_cache(city, payload, filepath)

    return WeatherResponse(source="openweather", data=payload, cached=False, saved_file=filepath)

@app.get("/")
async def root():
    return {"msg": "Weather API. Use GET /weather?city=London"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)