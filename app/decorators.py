from functools import wraps
from flask import request, abort

def wymagany_parametr(nazwa):
    def decorator(widok):
        @wraps(widok)
        def wrapper(*args, **kwargs):
            if nazwa not in request.args:
                abort(400, description=f"Brak parametru {nazwa}")
            return widok(*args, **kwargs)
        return wrapper
    return decorator