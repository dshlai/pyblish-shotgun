import os
import sys

from lib import (get_primary_pipeline_config,
                 platform_lookup,
                 append_pipeline_sgtk,
                 get_sg,
                 get_tk)

test_path = r"P:\projects\CM\shots\sq00\sq00_sh0560\light".replace("/", "\\")


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

    # Here our toolkit object is already authenticated in the pipeline configuration, yours may vary.
    context = tk.context_from_path(test_path)

    print context


def test_get_prime_pc():
    assert os.path.isdir(get_primary_pipeline_config(test_path).get(platform_lookup[sys.platform]))


def test_host():
    from shotgun_api3 import Shotgun
    fail_case_sg1 = Shotgun("", "", "")


if __name__ == '__main__':
    test_host()
