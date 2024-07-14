# import dependencies
import base64
import json

from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
from pywidevine import RemoteCdm
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
                    headers: str = None, json_data: str = None, cookies_data: str = None, input_data: str = None, wvd: str = None, proxy: str = None,):
    # prepare pssh
    try:
        pssh = PSSH(in_pssh)
    except Exception as error:
        return {
            'Message': str(error)
        }

    if wvd != 'Remote':

        # load device
        device = Device.load(wvd)

        # load CDM from device
        cdm = Cdm.from_device(device)

    else:
        cdm = RemoteCdm(
            device_type='ANDROID',
            system_id=int(requests.post(url='https://cdrm-project.com/devine').content),
            security_level=3,
            host='https://cdrm-project.com/devine',
            secret='CDRM-Project',
            device_name='CDM'
        )

    # open CDM session
    session_id = cdm.open()

    # Generate the challenge
    challenge = cdm.get_license_challenge(session_id, pssh)

    challenge_not_in_data = False
    extra_data_challenge = False

    if headers != '':
        try:
            headers = ast.literal_eval(clean_my_dict(dirty_dict=headers))

            # Iterate through the dictionary
            for key, value in headers.items():
                # Check if the value is '!Challenge'
                if value == '!Challenge':
                    # Replace the value with something else
                    headers[key] = base64.b64encode(challenge).decode()
                    challenge_not_in_data = True
        except:
            return {
                'Message': 'Headers could not be loaded correctly, please make sure they are formatted in python dictionary'
            }

    if json_data != '':
        try:
            json_data = ast.literal_eval(clean_my_dict(dirty_dict=json_data))
            # Iterate through the dictionary
            for key, value in json_data.items():
                # Check if the value is '!Challenge'
                if value == '!Challenge':
                    # Replace the value with something else
                    json_data[key] = base64.b64encode(challenge).decode()
                    challenge_not_in_data  = True
        except:
            return {
                'Message': 'JSON could not be loaded correctly, please make sure they are formatted in python dictionary format'
            }

    if cookies_data != '':
        try:
            cookies_data = ast.literal_eval(clean_my_dict(dirty_dict=cookies_data))
            # Iterate through the dictionary
            for key, value in cookies_data.items():
                # Check if the value is '!Challenge'
                if value == '!Challenge':
                    # Replace the value with something else
                    cookies_data[key] = base64.b64encode(challenge).decode()
                    challenge_not_in_data = True
        except:
            return {
                'Message': 'Cookies could not be loaded correctly, please make sure they are formatted in python dictionary format'
            }

    if input_data != '':
        try:
            input_data = ast.literal_eval(clean_my_dict(dirty_dict=input_data))
            # Iterate through the dictionary
            for key, value in input_data.items():
                # Check if the value is '!Challenge'
                if value == '!Challenge':
                    # Replace the value with something else
                    input_data[key] = base64.b64encode(challenge).decode()
                    extra_data_challenge = True
        except:
            return {
                'Message': 'Data could not be loaded correctly, please make sure they are formatted in python dictionary format'
            }

    # Try statement here, probably the most common point of failure
    try:
        if extra_data_challenge == False:
            if challenge_not_in_data == False:

                # send license challenge
                license = requests.post(
                    url=license_url,
                    headers=headers,
                    json=json_data,
                    cookies=cookies_data,
                    data=challenge,
                    proxies={
                        'http': proxy,
                    }
                )
            else:
                license = requests.post(
                    url=license_url,
                    headers=headers,
                    json=json_data,
                    cookies=cookies_data,
                    proxies={
                        'http': proxy,
                    }
                )
        else:
            print("Extra challenge!!")
            # send license challenge
            license = requests.post(
                url=license_url,
                headers=headers,
                json=json_data,
                cookies=cookies_data,
                data=input_data,
                proxies={
                    'http': proxy,
                }
            )
            if license.status_code != 200:
                license = requests.post(
                    url=license_url,
                    headers=headers,
                    json=json_data,
                    cookies=cookies_data,
                    data=json.dumps(input_data),
                    proxies={
                        'http': proxy,
                    }
                )


    except Exception as error:
        return {
            'Message': f'An error occured {error}\n\n{license.content}'
        }

    # Another try statement to parse licenses
    try:
        cdm.parse_license(session_id, license.content)
    except:
        try:
            cdm.parse_license(session_id, license.json().get('license'))
        except:
            try:
                replaced_license = license.json()["license"].replace("-", "+").replace("_", "/")
                cdm.parse_license(session_id, replaced_license)
            except:
                try:
                    cdm.parse_license(session_id, license.json().get('licenseData'))
                except:
                    try:
                        cdm.parse_license(session_id, license.json().get('widevine2License'))
                    except:
                        try:
                            cdm.parse_license(session_id, license.json().get('license')[0])
                        except Exception as error:
                            return {
                                'Message': f'An error occured {error}\n\n{license.content}'
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
