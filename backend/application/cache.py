import json
from functools import wraps
from flask import request, jsonify
from redis import Redis
from .config import LocalDevelopmentConfig

# initialize a global redis client using the configured URL
redis_client = Redis.from_url(LocalDevelopmentConfig.REDIS_URL, decode_responses=True)


def cache_response(expire: int = 60):
    """Decorator to cache the JSON response of a route for *expire* seconds.

    The cache key is derived from the request path and query string so that
    different parameters are cached separately.
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = f"cache:{request.full_path}"
            try:
                cached = redis_client.get(key)
                if cached:
                    return jsonify(json.loads(cached))
            except Exception:
                # if redis is unavailable just proceed normally
                pass

            response = f(*args, **kwargs)
            # only cache successful json responses
            try:
                if response.status_code == 200:
                    redis_client.setex(key, expire, json.dumps(response.get_json()))
            except Exception:
                pass
            return response
        return wrapped
    return decorator
