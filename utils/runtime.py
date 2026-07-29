'''
A place to store utility functions and / or objects that have to do with the application.
'''

from flask_limiter import Limiter
from flask_ipban import IpBan
from flask import Response

# === Rate-Limiting / banning utilities ===

# Our banner:
ip_ban = IpBan(ban_count = 6)

# Our rate-limiter - adjust when necessary:
limiter = Limiter(key_func = lambda x : 'global', default_limits = ['10 per hour'])

# Anon. function to successful requests:
def on_200(resp: Response) -> bool:
    return resp.status_code == 200

# === END === 