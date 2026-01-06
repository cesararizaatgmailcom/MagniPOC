import os
import re

def test_cartographer_yaml_present():
    path = os.path.join(os.path.dirname(__file__), '..', 'params', 'cartographer_params.yaml')
    path = os.path.normpath(path)
    assert os.path.exists(path), f"Missing {path}"


def test_yaml_references_lua():
    yaml_path = os.path.join(os.path.dirname(__file__), '..', 'params', 'cartographer_params.yaml')
    yaml_path = os.path.normpath(yaml_path)
    with open(yaml_path, 'r') as f:
        text = f.read()
    assert 'magni_2d.lua' in text, 'cartographer_params.yaml should reference magni_2d.lua'


def test_lua_config_sanity():
    lua_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'magni_2d.lua')
    lua_path = os.path.normpath(lua_path)
    assert os.path.exists(lua_path), f"Missing {lua_path}"
    with open(lua_path, 'r') as f:
        text = f.read()

    min_match = re.search(r'TRAJECTORY_BUILDER_2D\.min_range\s*=\s*([0-9]*\.?[0-9]+)', text)
    max_match = re.search(r'TRAJECTORY_BUILDER_2D\.max_range\s*=\s*([0-9]*\.?[0-9]+)', text)
    num_acc_match = re.search(r'TRAJECTORY_BUILDER_2D\.num_accumulated_range_data\s*=\s*([0-9]+)', text)

    assert min_match, 'min_range not found in maga_2d.lua'
    assert max_match, 'max_range not found in magni_2d.lua'
    assert num_acc_match, 'num_accumulated_range_data not found in magni_2d.lua'

    min_range = float(min_match.group(1))
    max_range = float(max_match.group(1))
    num_acc = int(num_acc_match.group(1))

    assert 0.0 < min_range < max_range, 'min_range should be >0 and < max_range'
    assert num_acc > 0, 'num_accumulated_range_data should be > 0'
