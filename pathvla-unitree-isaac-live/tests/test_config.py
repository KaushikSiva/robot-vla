from isaac_ext.pathvla_unitree.tasks.room_nav_env_cfg import (
    load_livestream_config,
    load_robot_config,
    load_scene_config,
    load_vla_config,
)


def test_scene_configs_load():
    assert load_scene_config("room").scene.name == "room"
    assert load_scene_config("warehouse").scene.name == "warehouse"


def test_other_configs_load():
    assert load_robot_config().robot.name == "unitree_g1"
    assert load_livestream_config().livestream.signaling_port == 8211
    assert load_vla_config().vla.request_timeout_s == 30
