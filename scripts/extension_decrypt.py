# import dependencies
import os
from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
import requests
import glob
from . import key_cache


# Defining decrypt function
def decrypt_content(in_pssh: str = None, license_url: str = None, headers: dict = None, wvd: str = None) -> list:

    # prepare pssh
    pssh = PSSH(in_pssh)

    # load device
    device = Device.load(wvd)

    # load CDM from device
    cdm = Cdm.from_device(device)

    # open CDM session
    session_id = cdm.open()

    # Generate the challenge
    challenge = cdm.get_license_challenge(session_id, pssh)

    # send license challenge
    license = requests.post(
        url=license_url,
        headers=headers,
        data=challenge
    )

    # Parse the license if it comes back in plain bytes
    try:
        cdm.parse_license(session_id, license.content)
    except:
        # Exception, try to find by regex via json
        try:
            cdm.parse_license(session_id, license.json()['license'])
        except:
            try:
                cdm.parse_license(session_id, license.json()['licenseData'])
            except Exception as error:
                return [error]


    # Assign variable for caching keys
    cached_keys = ""


    for key in cdm.get_keys(session_id):
        if key.type != "SIGNING":
            cached_keys += f"{key.kid.hex}:{key.key.hex()}\n"

    # Cache the keys
    key_cache.cache_keys(pssh=in_pssh, keys=cached_keys)

    # close session, disposes of session data
    cdm.close(session_id)

    # Return the keys
    return cached_keys
