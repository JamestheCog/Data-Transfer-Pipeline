'''
A module to contain handlers for errors and requests post-processing.
'''

from flask import Blueprint, jsonify, Response
from werkzeug.exceptions import HTTPException
from typing import Tuple
import json

general = Blueprint('middleware', __name__)

# Our app.'s error handler - catch all exceptions bubbled up here:
@general.app_errorhandler(HTTPException)
def err_handler(e: HTTPException):
    resp = {'error': ''}
    match e.code:
        case 429:
            resp['error'] = 'Back off, man.  Let me work.'
        case 403:
            resp['error'] = 'Begone, impostor!'
        case 404:
            resp['error'] = "You've gone astray!"
        case _:
            resp['error'] = 'What did you do, dude >:('
    return jsonify(resp), e.code

# Our app.'s handler for everything else:
@general.after_app_request
def capture_data(resp: Response) -> Response:
    '''
    General-purpose middleware - just captures success messages and returns them to the 
    client as JSON for now.
    '''
    msg = resp.get_data(as_text = True)
    resp.set_data(json.dumps({'msg': msg}))
    resp.headers['Content-Type'] = 'application/json'
    return resp
