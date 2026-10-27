"""Dependency minimums and the vulnerability scan in this repository's CI."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def declared_dependencies() -> list[str]:
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    block = re.search(r"^dependencies = \[\n(.*?)^\]", text, re.S | re.M)
    assert block is not None, "pyproject.toml: no [project] dependencies list"
    return re.findall(r'"([^"]+)"', block.group(1))


def test_dependency_minimums_admit_no_known_vulnerability() -> None:
    # certifi, idna, anyio and h11 come with httpx; they are declared so that
    # installing the package upgrades a release with a vulnerability known at
    # the time of this release.
    assert declared_dependencies() == [
        "httpx>=0.26,<1",
        "websockets>=15,<18",
        "anyio>=4.14.2",
        "h11>=0.16",
        "certifi>=2026.10.19",
        "idna>=3.15",
    ]


def test_ci_fails_on_any_known_vulnerability() -> None:
    workflow_file = ROOT / ".github" / "workflows" / "ci.yml"
    if not workflow_file.is_file():
        pytest.skip("The CI workflow is not part of this source tree (for example an sdist)")
    workflow = workflow_file.read_text(encoding="utf-8")
    audit = "python -m pip_audit --strict --no-deps --disable-pip --requirement"
    # The newest versions CI installs, development tools included.
    assert 'python -m pip freeze --exclude-editable > "$RUNNER_TEMP/installed.txt"' in workflow
    assert f'{audit} "$RUNNER_TEMP/installed.txt"' in workflow
    # Every dependency at the lowest version the package allows.
    assert "--resolution lowest-direct" in workflow
    assert f'{audit} "$RUNNER_TEMP/lowest.txt"' in workflow
