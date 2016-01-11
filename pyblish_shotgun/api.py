import yaml
import os
import logging

from shotgun_api3 import Shotgun

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

api_file = "U:/pipeline_configurations/StudioCore/config/core/shotgun.yml"  # change the name of the api key file


def get_api_data(__api_file=""):
    """
    function that reads secure api data such as key, script name, and host url.

    Returns:
        str: api_key,
        str: api_script,
        str: host
    """

    # if provided file is not a valid path then we use the hard coded one
    if not os.path.isfile(__api_file):
        __api_file = api_file

    with open(__api_file, 'r') as reader:
        data = yaml.load(reader)

    return data.get('api_key'), data.get('api_script'), data.get('host')


def get_sg_with_user(host="", login="", password=""):
    """
    Get Shotgun API object using username and password.
    Shotgun initialization should fail if one of the data provided is not valid

    Args:
            str: host (Host URL)
            str: user (Username)
            str: password (Password)

    Returns:
            shotgun_api3.shotgun.Shotgun: Shotgun API Instance

    Raises:
            ValueError: must provide login/password, session_token or script_name/api_key

    """

    return Shotgun(base_url=host, login=login, password=password)


def get_sg_with_key(host="", script="", key=""):
    """
    Get Shotgun API object using global api key.
    Shotgun initialization should fail if one of the data provided is not valid

    Args:
            str: host (Host URL)
            str: script (API Script Name)
            str: key (API Key)

    Returns:
            shotgun_api3.shotgun.Shotgun: Shotgun API Instance

    Raises:
            ValueError: must provide login/password, session_token or script_name/api_key

    """

    return Shotgun(host, script, key)
