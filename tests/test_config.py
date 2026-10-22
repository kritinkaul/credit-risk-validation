from pathlib import Path

import pytest
import yaml

from credit_risk.config import ConfigError, load_config

ROOT = Path(__file__).resolve().parents[1]


def write_config(tmp_path, payload):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(payload))
    return path


def test_foundation_accepts_explicit_unresolved_fields():
    config = load_config(ROOT / "configs/base.yaml")
    assert config.target.horizon_days is None
    assert config.evaluation.split_strategy == "pending"


@pytest.mark.parametrize(
    ("section", "field", "value"),
    [
        ("target", "horizon_days", 0),
        ("target", "horizon_days", -1),
        ("target", "horizon_days", True),
        ("target", "horizon_days", "90"),
        ("target", "horizon_days", 1.5),
        ("dataset", "name", ""),
        ("dataset", "source", "   "),
        ("dataset", "source", 123),
        ("evaluation", "split_strategy", "random"),
        ("storage", "engine", "postgres"),
        ("storage", "path", None),
        ("project", "stage", "trained"),
        ("project", "name", "other"),
    ],
)
def test_invalid_nested_values(tmp_path, payload, section, field, value):
    payload[section][field] = value
    with pytest.raises(ConfigError, match="Schema validation failed"):
        load_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("value", [-1, True, "42", 2**32])
def test_invalid_seed(tmp_path, payload, value):
    payload["random_seed"] = value
    with pytest.raises(ConfigError):
        load_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("section", ["project", "dataset", "target", "evaluation", "storage"])
def test_required_sections(tmp_path, payload, section):
    del payload[section]
    with pytest.raises(ConfigError, match="missing"):
        load_config(write_config(tmp_path, payload))


@pytest.mark.parametrize("section", ["dataset", "target", "evaluation", "storage"])
def test_required_nested_fields(tmp_path, payload, section):
    del payload[section][next(iter(payload[section]))]
    with pytest.raises(ConfigError, match="missing"):
        load_config(write_config(tmp_path, payload))


def test_unknown_fields_rejected(tmp_path, payload):
    payload["target"]["horizion_days"] = 90
    with pytest.raises(ConfigError, match="extra_forbidden"):
        load_config(write_config(tmp_path, payload))


@pytest.mark.parametrize(
    ("strategy", "column"),
    [("temporal", "observation_timestamp_column"), ("grouped", "borrower_id_column")],
)
def test_split_requires_column(tmp_path, payload, strategy, column):
    payload["evaluation"]["split_strategy"] = strategy
    with pytest.raises(ConfigError, match="value_error"):
        load_config(write_config(tmp_path, payload))
    payload["evaluation"][column] = "example_column"
    assert load_config(write_config(tmp_path, payload)).evaluation.split_strategy == strategy


def test_positive_horizon_is_structurally_valid(tmp_path, payload):
    # Arbitrary synthetic schema example, not a selected research horizon.
    payload["target"]["horizon_days"] = 7
    assert load_config(write_config(tmp_path, payload)).target.horizon_days == 7


@pytest.mark.parametrize(
    "content",
    [
        "",
        "[]",
        "42",
        "target: [",
        "a: 1\na: 2",
        "target:\n  a: 1\n  a: 2",
        "? [a, b]\n: c",
        "!!python/object/apply:os.system ['echo unsafe']",
    ],
)
def test_invalid_or_unsafe_yaml(tmp_path, content):
    path = tmp_path / "bad.yaml"
    path.write_text(content)
    with pytest.raises(ConfigError):
        load_config(path)


def test_unreadable_file_and_encoding(tmp_path):
    with pytest.raises(ConfigError, match="FileNotFoundError"):
        load_config(tmp_path / "absent.yaml")
    path = tmp_path / "binary.yaml"
    path.write_bytes(b"\xff")
    with pytest.raises(ConfigError, match="UnicodeDecodeError"):
        load_config(path)


def test_errors_do_not_echo_invalid_values(tmp_path, payload):
    payload["random_seed"] = "example-private-value"
    with pytest.raises(ConfigError) as error:
        load_config(write_config(tmp_path, payload))
    assert "example-private-value" not in str(error.value)
