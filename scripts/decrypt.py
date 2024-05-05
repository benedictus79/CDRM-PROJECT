# import dependencies
import base64
from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import requests
import ast
from . import key_cache


# Define a function to clean dictionary values sent as string from the post request
def clean_my_dict(dirty_dict: str = None):
    header_string = f"'''" \
                    f"{dirty_dict}" \
                    f"'''"
    cleaned_string = '\n'.join(line for line in header_string.split('\n') if not line.strip().startswith('#'))
    clean_dict = ast.literal_eval(cleaned_string)
    return clean_dict


# Defining decrypt function
def decrypt_content(in_pssh: str = None, license_url: str = None,
                    headers: str = None, json_data: str = None, wvd: str = None):
    # prepare pssh
    try:
        pssh = PSSH(in_pssh)
    except Exception as error:
        return {
            'Message': str(error)
        }

    # load device
    device = Device.load(wvd)

    # load CDM from device
    cdm = Cdm.from_device(device)

    # open CDM session
    session_id = cdm.open()

    # Generate the challenge
    challenge = cdm.get_license_challenge(session_id, pssh)

    if headers != '':
        try:
            headers = ast.literal_eval(clean_my_dict(dirty_dict=headers))
            print(headers)
        except:
            return {
                'Message': 'Headers could not be loaded correctly, please make sure they are formatted in python dictionary'
            }

    if json_data != '':
        try:
            json_data = ast.literal_eval(clean_my_dict(dirty_dict=json_data))
            print(json_data)
        except:
            return {
                'Message': 'JSON could not be loaded correctly, please make sure they are formatted in python dictionary format'
            }

    # Try statement here, probably the most common point of failure
    try:
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            json=json_data,
            data=challenge
        )
    except Exception as error:
        return {
            'Message': str(error)
        }

    # Another try statement to parse licenses
    try:
        cdm.parse_license(session_id, license.content)
    except:
        try:
            cdm.parse_license(session_id, license.json().get('license'))
        except:
            try:
                cdm.parse_license(session_id, license.json().get('licenseData'))
            except:
                try:
                    cdm.parse_license(session_id, license.json().get('widevine2License'))
                except Exception as error:
                    return {
                        'Message': str(error)
                    }

    # assign variable for returned keys
    returned_keys = ""
    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            returned_keys += f"{key.kid.hex}:{key.key.hex()}\n"

    # close session, disposes of session data
    cdm.close(session_id)

    # Cache the keys
    key_cache.cache_keys(pssh=in_pssh, keys=returned_keys)

    # Return the keys
    return {
        'Message': returned_keys
    }
