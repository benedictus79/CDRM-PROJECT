# Import dependencies
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file, Response, current_app
import scripts
import uuid
import json
import base64
from pywidevine import __version__
from pywidevine.pssh import PSSH
from pywidevine.cdm import Cdm
from pywidevine.device import Device
from pywidevine.exceptions import (InvalidContext, InvalidInitData, InvalidLicenseMessage, InvalidLicenseType,
                                   InvalidSession, SignatureMismatch, TooManySessions)

# Create database if it doesn't exist
scripts.create_database.create_database()

# Check for .WVD file and assign it a variable
WVD = scripts.wvd_check.check_for_wvd()

# If no WVD found, exit
if WVD is None:
    exit("No .wvd file found, please place one in /databases/WVDs and try again.")

# Define Flask app object, give template and static arguments.
app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')

# Create a secret key for logins
app.secret_key = str(uuid.uuid4())

# Route for root '/'
@app.route("/", methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':

        # Get the JSON data from the request
        data = json.loads(request.data.decode())

        # Get the proxy
        proxy = data['Proxy']
        if proxy == '':
            proxy = None

        decrypt_response = scripts.decrypt.decrypt_content(
            in_pssh=request.json['PSSH'],
            license_url=request.json['License URL'],
            headers=request.json['Headers'],
            json_data=request.json['JSON'],
            cookies_data=request.json['Cookies'],
            input_data=request.json['Data'],
            wvd=WVD,
            proxy=proxy,
        )
        return jsonify(decrypt_response)


# Route for '/cache'
@app.route("/cache", methods=['GET'])
def cache_page():
    if request.method == 'GET':
        cache_page_key_count = scripts.key_count.count_keys()
        return render_template('cache.html', cache_page_key_count=cache_page_key_count)

@app.route("/key_count", methods=['GET'])
def key_count():
    if request.method == 'GET':
        results = scripts.key_count.count_keys()
        results = 'Total Keys: ' + str(results)
        message = {
            'Message': results
        }
        return jsonify(message)

# Route for '/faq'
@app.route("/faq", methods=['GET'])
def faq_page():
    if request.method == 'GET':
        return render_template('faq.html')


@app.route("/api", methods=['GET', 'POST'])
def api_page():
    if request.method == 'GET':
        return render_template('api.html')
    elif request.method == 'POST':
        return


@app.route("/extension", methods=['GET', 'POST'])
def extension_page():
    if request.method == 'GET':
        return render_template('extension.html')

    elif request.method == 'POST':
        # Get the JSON data from the request
        data = json.loads(request.data.decode())

        # Get the PSSH
        pssh = data['PSSH']

        # Get the license URL
        lic_url = data['License URL']

        # Get the headers
        headers = data['Headers']
        headers = json.loads(headers)

        # Get the MPD url
        json_data = data['JSON']
        if json_data:
            try:
                json_data = base64.b64decode(json_data).decode()
                json_data = json.loads(json_data)
            except:
                json_data = json_data

        # Get the proxy
        proxy = data['Proxy']
        if proxy == '':
            proxy = None

        if data['Scheme'] == 'CommonWV':
            try:
                keys = scripts.extension_decrypt.decrypt_content(in_pssh=pssh, license_url=lic_url, headers=headers,
                                                                 wvd=WVD, scheme=data['Scheme'], proxy=proxy)
                return {'Message': f'{keys}'}
            except Exception as error:
                return {"Message": [f'{error}']}

        if data['Scheme'] == 'Amazon':
            try:
                keys = scripts.extension_decrypt.decrypt_content(in_pssh=pssh, license_url=lic_url, headers=headers,
                                                                 wvd=WVD, scheme=data['Scheme'], proxy=proxy)
                return {'Message': f'{keys}'}
            except Exception as error:
                return {"Message": [f'{error}']}

        if data['Scheme'] == 'YouTube':
            try:
                print(data['Scheme'])
                keys = scripts.extension_decrypt.decrypt_content(in_pssh=pssh, license_url=lic_url, headers=headers,
                                                                 wvd=WVD, scheme=data['Scheme'], proxy=proxy, json_data=json_data)
                print(json_data)
                return {'Message': f'{keys}'}
            except Exception as error:
                return {"Message": [f'{error}']}


@app.route("/download-extension", methods=['GET', 'POST'])
def download_extension_page():
    if request.method == 'GET':
        file_path = 'static/assets/wvg-next-cdrm.zip'
        return send_file(file_path, as_attachment=True)
    elif request.method == 'POST':
        version = {
            'Version': '1.11'
        }
        return jsonify(version)


# Route for '/login'
@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect('/profile')
        else:
            return render_template('login.html')
    if request.method == 'POST':
        username = request.json['Username']
        if scripts.check_user.check_username_exist(username=username.lower()):
            if scripts.check_user.check_password(username=username.lower(), password=request.json['Password']):
                session['logged_in'] = True
                return {
                    'Message': 'Success'
                }
            else:
                return {
                    'Message': 'Failed to Login'
                }
        else:
            return {
                'Message': 'Username does not exist'
            }


# Route for '/register'
@app.route("/register", methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.json['Username']
        if username == '':
            return {
                'Message': 'Username cannot be empty'
            }
        if not scripts.check_user.check_username_exist(username=username.lower()):
            scripts.check_user.insert_user(username=username.lower(), password=request.json['Password'])
            session['logged_in'] = True
            return {
                'Message': 'Success'
            }
        else:
            return {
                'Message': 'Username already taken'
            }


# Route for '/profile'
@app.route("/profile", methods=['GET'])
def profile():
    if request.method == 'GET':
        return render_template('profile.html')


# Route for '/devine'
@app.route("/devine", methods=['GET', 'POST', 'HEAD'])
def devine_page():
    if request.method == 'GET':
        cdm = Cdm.from_device(device=Device.load(WVD))
        cdm_version = cdm.system_id
        devine_service_count = scripts.key_count.get_service_count_devine()
        devine_key_count = scripts.key_count.count_keys_devine()
        return render_template('devine.html', cdm_version=cdm_version, devine_service_count=devine_service_count, devine_key_count=devine_key_count)
    if request.method == 'POST':
        return
    if request.method == 'HEAD':
        response = Response(status=200)
        response.headers.update({
            "Server": f"https://github.com/devine-dl/pywidevine serve v{__version__}"
        })
        return response


# Route for '/{device}/open'
@app.route("/devine/<device>/open", methods=['GET'])
def device_open(device):
    if request.method == 'GET':
        cdm_device = Device.load(WVD)
        cdm = current_app.config['cdms'] = Cdm.from_device(cdm_device)
        session_id = cdm.open()
        response_data = {
            "status": 200,
            "message": "Success",
            "data": {
                "session_id": session_id.hex(),
                "device": {
                    "system_id": cdm.system_id,
                    "security_level": cdm.security_level
                    }
                }
            }
        return jsonify(response_data)


# Route for '/{device}/set_service_certificate'
@app.route("/devine/<device>/set_service_certificate", methods=['POST'])
def set_cert(device):
    if request.method == 'POST':
        cdm = current_app.config["cdms"]
        body = request.json

        # get session id
        session_id = bytes.fromhex(body["session_id"])

        # set service certificate
        certificate = body.get("certificate")

        provider_id = cdm.set_service_certificate(session_id, certificate)

        response_data = {
            "status": 200,
            "message": f"Successfully {['set', 'unset'][not certificate]} the Service Certificate.",
            "data": {
                "provider_id": provider_id
            }
        }

        return jsonify(response_data)


@app.route("/devine/<device>/get_license_challenge/<licensetype>", methods=['POST'])
def get_license_challenge_page(device, licensetype):
    if request.method == 'POST':
        cdm = current_app.config["cdms"]

        body = request.json

        session_id = bytes.fromhex(body["session_id"])

        privacy_mode = body.get("privacy_mode", True)

        current_app.config['PSSH'] = body['init_data']
        init_data = PSSH(body["init_data"])

        license_request = cdm.get_license_challenge(
            session_id=session_id,
            pssh=init_data,
            license_type=licensetype,
            privacy_mode=privacy_mode
        )

        results = {
            "status": 200,
            "message": "Success",
            "data": {
                "challenge_b64": base64.b64encode(license_request).decode()
            }
        }

        return jsonify(results)


@app.route("/devine/<device>/parse_license", methods=['POST'])
def parse_license(device):
    if request.method == 'POST':
        cdm = current_app.config["cdms"]

        body = request.json

        session_id = bytes.fromhex(body["session_id"])

        cdm.parse_license(session_id, body["license_message"])

        results = {
            "status": 200,
            "message": "Successfully parsed and loaded the Keys from the License message."
        }

        return jsonify(results)


@app.route("/devine/<device>/get_keys/<key_type>", methods=['POST'])
def get_keys(device, key_type):
    if request.method == 'POST':
        cdm = current_app.config["cdms"]

        body = request.json

        session_id = bytes.fromhex(body["session_id"])

        if key_type == "ALL":
            key_type = None

        keys = cdm.get_keys(session_id, key_type)
        returned_keys = ""
        for key in cdm.get_keys(session_id):
            if key.type != "SIGNING":
                returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"

        keys_json = [
            {
                "key_id": key.kid.hex,
                "key": key.key.hex(),
                "type": key.type,
                "permissions": key.permissions,
            }
            for key in keys
            if not key_type or key.type == key_type
        ]

        results = {
            "status": 200,
            "message": "Success",
            "data": {
                "keys": keys_json
            }
        }

        scripts.key_cache.cache_keys(pssh=current_app.config['PSSH'], keys=returned_keys)

        return jsonify(results)


@app.route("/devine/<device>/close/<session_id>", methods=['GET'])
def close_session(device, session_id):
    if request.method == 'GET':
        cdm = current_app.config["cdms"]

        session_id = bytes.fromhex(session_id)

        cdm.close(session_id)

        results = {
            "status": 200,
            "message": f"Successfully closed Session '{session_id.hex()}'."
        }

        return jsonify(results)

@app.route("/devine/vault/<service>", methods=['POST'])
def add_keys_devine_vault(service):
    data = request.json['content_keys']
    replaced = 0
    inserted = 0
    for key_id, key in data.items():
        result = scripts.key_cache.cache_keys_devine(service=service, kid=key_id, key=key)
        if result == 'inserted':
            inserted += 1
        if result == 'replaced':
            replaced += 1

    message = {
        "code": 0,
        "added": inserted,
        "updated": replaced
    }
    return jsonify(message)

@app.route("/devine/vault/<service>/<kid>", methods=['GET'])
def get_key_devine_vault(service, kid):
    key = scripts.vault_check.get_key_by_kid_and_service(service=service, kid=kid)
    message = {
        "code": 0,
        "content_key": key
    }
    return jsonify(message)


# If the script is called directly, start the flask app.
if __name__ == '__main__':
    app.run(debug=True)
