import time, asyncio
from typing import Dict
from .config import settings

_requests: Dict[str, list] = {}
_lock = asyncio.Lock()

async def allow_request(client_id: str) -> bool:
    now = time.time()
    window = 60
    limit = settings.rate_limit_per_minute
    async with _lock:
        history = _requests.get(client_id, [])
        # remove old entries
        history = [t for t in history if t > now - window]
        if len(history) >= limit:
            _requests[client_id] = history
            return False
        history.append(now)
        _requests[client_id] = history
        return True