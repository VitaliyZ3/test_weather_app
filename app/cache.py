import asyncio, time
from typing import Any, Dict, Tuple

_cache: Dict[str, Tuple[float, Any, str]] = {}
_lock = asyncio.Lock()

async def get_cached(city: str, ttl_seconds: int):
    async with _lock:
        entry = _cache.get(city.lower())
        if not entry:
            return None
        ts, payload, saved_file = entry
        if time.time() - ts < ttl_seconds:
            return {"timestamp": ts, "payload": payload, "saved_file": saved_file}
        else:
            # removing the staled data
            del _cache[city.lower()]
            return None

async def set_cache(city: str, payload: Any, saved_file: str):
    async with _lock:
        _cache[city.lower()] = (time.time(), payload, saved_file)