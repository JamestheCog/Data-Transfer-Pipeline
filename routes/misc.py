'''
Routes for other stuff that don't fit nicely within the app.'s intended use cases - including health checks.
Note that I didn't include a wake-up route as the app.'s gonna awaken when somebody pings it anyways (successful 
or not).  Worst comes to worst, a minute of runtime is consumed at most (i.e., there's not really a way to mitigate
DoS attacks save for relying on Render's built-in defenses).
'''

from flask import Blueprint, request, abort, current_app
from utils import db, runtime
import json

misc = Blueprint(__name__, 'misc')

@misc.route('/health', methods = ['POST'])
@runtime.limiter('1 per hour', deduct_when = runtime.on_200)
def health():
    '''
    Route logic for health check - functions below initial req. check 
    will throw if anything's gone wrong.  Add on more functions in 
    the future if need be!
    '''
    try:
        app_vals = current_app.config['APP_VALUES']
        data = request.get_json()
        if data.get('authorization').get('password') != app_vals['HEALTH_PASS']:
            runtime.ip_ban.add()
            abort(400, "You're not my doctor!")

        db.check_health(app_vals['DB_CONN_URI'], app_vals['DB_CONN_STRING'])
        return "No sick days for this application!", 200
    except json.decoder.JSONDecodeError:
        abort(500, "I can't read.")
    except AttributeError:
        abort(400, 'What the heck DID you send over?')
    except Exception as e:
        current_app.logger.error(f"Le patient's complaints: {str(e)}")
        abort(500, 'As healthy as a Big Mac.  Yep.')