from pydantic import BaseModel
from typing import Any, Dict

class WeatherResponse(BaseModel):
    source: str
    data: Dict[str, Any]
    cached: bool = False
    saved_file: str | None = None