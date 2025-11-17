import os, json, datetime
from .config import settings
from pathlib import Path
from typing import Tuple

Path(settings.data_dir).mkdir(parents=True, exist_ok=True)

def save_weather_response(city: str, payload: dict) -> Tuple[str, str]:
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    safe_city = city.replace(" ", "_").lower()
    filename = f"{safe_city}_{ts}.json"
    filepath = os.path.join(settings.data_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump({"timestamp": ts, "city": city, "payload": payload}, f, ensure_ascii=False, indent=2)
    return filepath, filename