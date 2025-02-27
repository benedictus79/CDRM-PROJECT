# import dependencies
from pywidevine import PSSH
from pywidevine import Cdm
from pywidevine import Device
from pywidevine import RemoteCdm
import requests
from . import key_cache
import base64
import tls_client
from xml.etree import ElementTree as ET

# Defining decrypt function
def decrypt_content(in_pssh: str = None, license_url: str = None, headers: dict = None, json_data: dict = None, wvd: str = None, scheme: str = None, proxy: str = None,):

    # prepare pssh
    pssh = PSSH(in_pssh)

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

    if scheme == 'CommonWV':
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            data=challenge,
            proxies={
                'http': proxy,
            },
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
                    return f'{error}\n\n{license.content}'

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

    if scheme == 'Amazon':
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            data={
                'widevine2Challenge': f'{base64.b64encode(challenge).decode()}',
                'includeHdcpTestKeyInLicense': 'true',
            },
            proxies={
                'http': proxy,
            }
        )

        # Parse the license if it comes back in plain bytes
        try:
            cdm.parse_license(session_id, license.json()['widevine2License']['license'])
        except Exception as error:
            return [f'{error}\n\n{license.content}']

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

    if scheme == 'YouTube':
        json_data['licenseRequest'] = base64.b64encode(challenge).decode()
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            json=json_data,
            proxies={
                'http': proxy,
            }
        )
        # Extract license from json dict
        license = license.json()["license"].replace("-", "+").replace("_", "/")

        # Parse the license if it comes back in plain bytes
        try:
            cdm.parse_license(session_id, license)
        except Exception as error:
            return f'{error}\n\n{license.content}'

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

    if scheme == 'RTE':
        json_data['getWidevineLicense']['widevineChallenge'] = base64.b64encode(challenge).decode()
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            json=json_data,
            proxies={
                'http': proxy,
            }
        )

        # Parse the license if it comes back in plain bytes
        try:
            cdm.parse_license(session_id, license.json()['getWidevineLicenseResponse']['license'])
        except Exception as error:
            return f'{error}\n\n{license.content}'

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

    if scheme == 'Canal+':

        try:
            json_data['ServiceRequest']['InData']['ChallengeInfo'] = base64.b64encode(challenge).decode()

            # send license challenge
            license = requests.post(
                url=license_url,
                headers=headers,
                json=json_data
            )

            # Parse the license
            try:
                cdm.parse_license(session_id, license.json()['ServiceResponse']['OutData']['LicenseInfo'])
            except Exception as error:
                return f'{error}\n\n{license.content}'

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

        except:

            try:
                session = tls_client.Session()

                response = session.post(
                    url=license_url,
                    headers=headers,
                    data=f'{base64.b64encode(challenge).decode()}'
                ).content.decode()

                # Define the namespace
                namespace = {'ns': 'http://www.canal-plus.com/DRM/V1'}

                # Parse the XML string
                root = ET.fromstring(response)

                # Find the license element using the namespace
                license_element = root.find('.//ns:license', namespace)

                # Extract the text content of the license element
                license_content = license_element.text

                # Parse the license
                try:
                    cdm.parse_license(session_id, license_content)
                except Exception as error:
                    return f'{error}\n\n{license.content}'

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

            except Exception as error:
                return [f'{error}\n\n{license.content}']

    if scheme == 'NosTV':
        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            json={
                'challenge': base64.b64encode(challenge).decode(),
            },
            proxies={
                'http': proxy,
            },
        )

        # Parse the license if it comes back in plain bytes
        try:
            cdm.parse_license(session_id, license.json()['license'][0])
        except Exception as error:
            return f'{error}\n\n{license.content}'

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

    if scheme == 'AstroGo':

        # Insert the challenge
        json_data['licenseChallenge'] = base64.b64encode(challenge).decode()

        # send license challenge
        license = requests.post(
            url=license_url,
            headers=headers,
            json=json_data,
            proxies={
                'http': proxy,
            },
        )

        # Parse the license if it comes back in plain bytes
        try:
            cdm.parse_license(session_id, license.content)
        except Exception as error:
            return f'{error}\n\n{license.content}'

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