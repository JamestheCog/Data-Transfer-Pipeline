from flask import Flask
from dotenv import load_dotenv
from routes import misc, receive, general
from cryptography.fernet import Fernet
from utils import runtime
import os, re, json

# --- Register application routes here---
app = Flask(__name__)
app.register_blueprint(misc.misc)
app.register_blueprint(receive.receive)
app.register_blueprint(general.general)
# --- END ---


# --- Implementing banning here ---
runtime.ip_ban.init_app(app, ban_count = 6)
# --- END ---


# --- Registering environment variables as app. config variables ---
load_dotenv()
required = ['MAX_FILE_SIZE',
            'FERNET_KEY', 'HEALTH_PASS'
            'FORMSG_URI', 'FORMSG_KEY', 'FORMSG_HEADERS',
            'DB_CONN_STRING', 'DB_CONN_URI']
required_vals = {}
for i in required:
    val = os.getenv(i)
    val = '' if not val else val.strip()
    required_vals[i] = float(val) if val and re.search(r'\d+(\.\d+)?$', val) else val

missing_vals = list(filter(lambda k : not required_vals[k], required_vals))
if len(missing_vals):
    error_msg = f"No env values for the following: {', '.join(missing_vals)}"
    app.logger.error(error_msg)
    raise RuntimeError(error_msg)
app.config['APP_VALUES'] = required_vals
# --- END ---


# --- Reading in and decrypting our files ---
'''
RESOURCE_DIR = './resources'
try:
    required_files, decryptor = {}, Fernet(rf"{required_vals.get('FERNET_KEY')}")
    for i in os.listdir(RESOURCE_DIR):
        i = i.lower()
        if not i.endswith('.json'):
            continue

        file_key = re.sub(r'_+', '_', '_'.join(i.split('.')[:-1]).strip())
        with open(os.path.join(RESOURCE_DIR, i)) as file:
            raw_text = file.read().strip()
            if not raw_text:
                raise Exception(f"File '{i}' is empty.")
            decrypted_text = decryptor.decrypt(rf'{raw_text}').decode('utf-8')
        required_files[file_key] = json.loads(decrypted_text)
    app.config['APP_FILES'] = required_files
except Exception as e:
    app.logger.error(f"Something went wrong during the decryption: {str(e)}")
    raise RuntimeError('Failed to decrypt the files - check the Fernet key and / or the logs!')
'''
# --- END ---


if __name__ == '__main__':
    app.run()