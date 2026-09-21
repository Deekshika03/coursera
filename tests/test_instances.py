"""Tests for multi-instance configuration loading and fallback."""

import json
from pathlib import Path

from coursera_automation.instances import InstanceConfig, load_instances


def test_load_instances_fallback(tmp_path: Path) -> None:
    """When json file is missing, fallback to single instance configuration."""
    missing = tmp_path / "nonexistent.json"
    instances = load_instances(str(missing))
    assert len(instances) == 1
    assert isinstance(instances[0], InstanceConfig)
    assert instances[0].email != ""


def test_load_instances_from_json(tmp_path: Path) -> None:
    """Correctly load and parse multiple instances from JSON file."""
    p = tmp_path / "test_instances.json"
    data = [
        {
            "email": "test1@cuchd.in",
            "password": "pass1",
            "course_url": "https://coursera.org/c1",
            "headless": True,
            "max_items": 10,
        },
        {
            "email": "test2@cuchd.in",
            "password": "pass2",
            "course_url": "https://coursera.org/c2",
            "headless": False,
            "max_items": 20,
        },
    ]
    p.write_text(json.dumps(data), encoding="utf-8")
    instances = load_instances(str(p))
    assert len(instances) == 2
    assert instances[0].email == "test1@cuchd.in"
    assert instances[0].max_items == 10
    assert instances[1].email == "test2@cuchd.in"
    settings = instances[0].to_settings()
    assert settings.email == "test1@cuchd.in"
    assert settings.headless is True
