# For now the best way to ask for the location of the pipeline configuration is to ask for it in the api.
# In order to setup API you will need api key and script name from the Shotgun
# we set it up in a separate data file

import os
import json
import sys
import collections

from shotgun_api3 import Shotgun

platform_lookup = {"linux2": "linux_path", "win32": "windows_path", "darwin": "mac_path"}

__PIPELINE_CONFIG_PATH__ = ""

api_file = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'key.json')  # change the name of the api key file


def get_api_data():
    """
    function that reads secure api data such as key, script name, and host url.
    :return:
    """
    with open(api_file, 'r') as reader:
        data = json.load(reader)

    return data.get('api_key'), data.get('api_script'), data.get('host')


def pipeline_config_from_path(sg, path):
    """
    Resolves the pipeline configs for a path
    Answer provided by Manne Ohrstrom
    """

    # get all local storages for this site
    local_storages = sg.find("LocalStorage",
                             [],
                             ["id", "code", "windows_path", "mac_path", "linux_path"])

    # get all pipeline configurations (and their associated projects) for this site
    pipeline_configs = sg.find("PipelineConfiguration",
                               [["project.Project.tank_name", "is_not", None]],
                               ["id", "code", "windows_path", "linux_path", "mac_path", "project",
                                "project.Project.tank_name"])


    # extract all storages for the current os
    storages = []

    for storage in local_storages:
        current_os_storage_path = storage[platform_lookup[sys.platform]]
        if current_os_storage_path:
            storages.append(current_os_storage_path)

    # build a dict of storage project paths and associate with project id
    project_paths = collections.defaultdict(list)

    for pc in pipeline_configs:
        for s in storages:
            # all pipeline configurations are associated
            # with a project which has a tank_name set
            project_path = os.path.join(s, pc["project.Project.tank_name"])
            # associate this path with the pipeline configuration
            project_paths[project_path].append(pc)

    # look at the path we passed in - see if any of the computed
    # project folders are determined to be a parent path
    for project_path in project_paths:
        # (like the SG API, this logic is case preserving, not case insensitive)
        if path.lower().startswith(project_path.lower()):
            # found a match! Return the associated list of pipeline configurations
            return project_paths[project_path]


def append_pipeline_sgtk(pipeline_path):
    pipeline_py_path = os.path.join(pipeline_path, "install/core/python")
    sys.path.append(pipeline_py_path)


def get_tk(path):
    # toolkit api object will fail without authentication, so you need authenticate before you can
    # use the toolkit api object. You can do that in the shotgun.yml in your pipeline configuration
    # or use the Shotgun Authentication library to construct a User object. Please see:
    #
    # https://support.shotgunsoftware.com/entries/95441317-An-overview-of-the-different-concepts-in-the-Shotgun-Pipeline-Toolkit#Security%20and%20Authentication

    sgtk = __import__('sgtk')
    tk = sgtk.sgtk_from_path(path)
    return tk


def get_sg():
    """
    Get Shotgun API object
    :return:
    """
    key, script, host = get_api_data()
    return Shotgun(host, script, key)


def get_primary_pipeline_config(path):
    """
    Return Primary pipeline configuration path from a given path
    :param path:
    :return:
    """
    pipeline_configs = pipeline_config_from_path(get_sg(), path)
    if pipeline_configs:
        for pc in pipeline_configs:
            if pc.get('code') == 'Primary':
                return pc


def pipeline_config_lookup(path, pipeline_code):
    """
    Return custom pipeline configuration path from a given path
    :param path:
    :param pipeline_code:
    :return:
    """
    pipeline_configs = pipeline_config_from_path(get_sg(), path)

    if pipeline_configs:
        for pc in pipeline_configs:
            if pc.get('code') == pipeline_code:
                return pc


def get_platform_pipeline_path(pipeline_config):
    """
    Get os specific pipeline configuration path
    :param pipeline_config:
    :return:
    """
    return pipeline_config.get(platform_lookup[sys.platform])
