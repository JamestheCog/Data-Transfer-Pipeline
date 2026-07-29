'''
A module to contain routes that have to do with the fetching of data from the form.gov.sg platform.
Note that I initialize the SDK here because it seems to go staler than yo momma's brussel sprouts
left in current_app.config.
'''

from flask import Blueprint, request, abort, current_app
import formsg, etl, json
from formsg.exceptions import WebhookAuthenticateException
from utils import files, runtime

receive = Blueprint('receive', __name__)
sdk = formsg.FormSdk('PRODUCTION')

@receive.route('/upload', methods = ['POST'])
@runtime.limiter.limit(None, deduct_when = runtime.on_200)
def upload_data():
    '''
    Note (Friday, 24th July, 2026): what was i supposed to do again lol
    '''
    data, data_size = request.data, request.content_length
    app_vals = current_app.config['APP_VALUES']
    if not data or files.to_mb(data_size) > app_vals['MAX_FILE_SIZE']:
        abort(400, 'Sent payload is invalid')

    try:
        data = json.loads(data)
        decrypt_key, uri = app_vals['FORMSG_KEY'], app_vals['FORMSG_URI']
        sdk.webhooks.authenticate(request.headers['X-FormSG-Signature'], uri)

        decrypted = sdk.crypto.decrypt(decrypt_key, data['data'])
        print(decrypted)
        # processed = etl.process(decrypted)
        # etl.load(processed)
        return 'Shit went well, man', 200
    except WebhookAuthenticateException, KeyError:
        runtime.ip_ban.add()
        abort(400, "Begone, and return with your papers!")
    except etl.exceptions.ProcessException as e:
        current_app.logger.error(f'Could not process the data: {str(e)}')
        abort(500, f"Processing")
    except etl.exceptions.LoadException as e:
        current_app.logger.error(f'Could not upload data to the DB: {str(e)}')
        abort(500, f"No uploady data to dee bee.")
    except Exception as e:
        current_app.logger.error(f'Something bad in general happened during the ETL process: {str(e)}')
        abort(500, f"Some-someTHing happened, big bro!")