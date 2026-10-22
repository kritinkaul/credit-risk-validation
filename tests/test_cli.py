import subprocess
import sys
from pathlib import Path

import pytest

from credit_risk.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_valid_config(capsys):
    assert main(["validate-config", str(ROOT / "configs/base.yaml")]) == 0
    assert "foundation schema only" in capsys.readouterr().out


def test_invalid_config(tmp_path, capsys):
    path = tmp_path / "invalid.yaml"
    path.write_text("{}")
    assert main(["validate-config", str(path)]) == 1
    assert "Invalid configuration" in capsys.readouterr().err


@pytest.mark.parametrize("arguments", [["--help"], ["validate-config", "--help"]])
def test_help(arguments, capsys):
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 0
    assert "usage:" in capsys.readouterr().out


@pytest.mark.parametrize("arguments", [[], ["train"], ["validate-config"]])
def test_usage_errors(arguments):
    with pytest.raises(SystemExit) as error:
        main(arguments)
    assert error.value.code == 2


def test_module_entrypoint_from_outside_repository(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "credit_risk", "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "validate-config" in result.stdout


def test_console_script_from_outside_repository(tmp_path):
    script = Path(sys.executable).parent / "credit-risk"
    result = subprocess.run(
        [str(script), "validate-config", str(ROOT / "configs/base.yaml")],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "no data or model evaluated" in result.stdout
