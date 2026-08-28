from __future__ import annotations

import subprocess

import pytest


def _docker(*args: str) -> str:
    result = subprocess.run(
        ["docker", *args], capture_output=True, text=True, shell=False, timeout=30, check=False
    )
    assert result.returncode == 0, result.stderr
    return result.stdout.strip()


@pytest.mark.runtime
def test_docker_health_and_final_p1_5_residue_are_clean() -> None:
    assert _docker("info", "--format", "{{.OSType}}") == "linux"
    assert _docker("ps", "-aq", "--filter", "label=aiscc.task=p1-5") == ""
    assert _docker("network", "ls", "-q", "--filter", "label=aiscc.task=p1-5") == ""
