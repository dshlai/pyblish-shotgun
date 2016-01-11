import os
import sys

from lib import (get_primary_pipeline_config,
                 platform_lookup,
                 append_pipeline_sgtk,
                 get_tk,
                 get_custom_tk)

from api import (get_api_data, get_sg_with_key, get_sg_with_user)

test_path = r"P:\projects\CM\shots\sq00\sq00_sh0560\light".replace("/", "\\")
test_file_path = r"P:\projects\CM\shots\sq00\sq00_sh0560\light\work\maya\sq00_sh560_nearB_light_v002.ma".replace("/", "\\")


def test_pipeline_config():
    pipeline_config = get_primary_pipeline_config(test_path)
    assert pipeline_config


def test_pipeline_path():
    pipeline_config = get_primary_pipeline_config(test_path)
    pipeline_path = pipeline_config.get(platform_lookup[sys.platform])
    assert pipeline_path


def test_get_pipeline_python():
    pipeline_config = get_primary_pipeline_config(test_path)
    pipeline_path = pipeline_config.get(platform_lookup[sys.platform])
    append_pipeline_sgtk(pipeline_path)
    tk = get_tk(test_path)
    assert tk


def test_path_context():
    pipeline_config = get_primary_pipeline_config(test_path)
    pipeline_path = pipeline_config.get(platform_lookup[sys.platform])
    append_pipeline_sgtk(pipeline_path)

    tk = get_tk(test_path)
    tk2 = get_tk(test_file_path)

    # Here our toolkit object is already authenticated in the pipeline configuration, yours may vary.
    context = tk.context_from_path(test_path)
    context2 = tk2.context_from_path(test_file_path)

    assert context == context2
    print context


def test_get_prime_pc():
    assert os.path.isdir(get_primary_pipeline_config(test_path).get(platform_lookup[sys.platform]))


def test_host():
    assert get_sg_with_key(*get_api_data())


def test_sg_with_user():
    from getpass import getpass
    host, script, key = get_api_data()
    # user = raw_input("User: ")
    # passwd = getpass()
    user = "test_user"
    passwd = "some pass"
    sg_inst = get_sg_with_user(host=host, login=user, password=passwd)
    # use test case should fail
    result = sg_inst.find("Shot", [], [])
    assert result


def test_custom_pc():
    custom_pc_path = os.path.join("U:\\", "pipeline_configurations", "CM")
    tk = get_custom_tk(test_file_path, custom_pc_path)
    assert tk


if __name__ == '__main__':
    test_host()
