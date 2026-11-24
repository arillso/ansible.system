"""Keep ``default:`` in meta/argument_specs.yml in line with defaults/main.yml.

The rendered role documentation shows the spec default, while the role uses
the value from defaults/main.yml. A spec default that differs from the role
default documents a value the role never applies.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROLES_DIR = Path(__file__).resolve().parents[2] / "roles"
ROLES = sorted(p.parent.parent.name for p in ROLES_DIR.glob("*/meta/argument_specs.yml"))


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


@pytest.mark.parametrize("role", ROLES)
def test_spec_defaults_match_role_defaults(role):
    specs = load_yaml(ROLES_DIR / role / "meta" / "argument_specs.yml")["argument_specs"]
    defaults_file = ROLES_DIR / role / "defaults" / "main.yml"
    role_defaults = (load_yaml(defaults_file) or {}) if defaults_file.exists() else {}

    drift = [
        f"{entry}.{name}"
        for entry, spec in specs.items()
        for name, option in (spec.get("options") or {}).items()
        if "default" in option and name in role_defaults and option["default"] != role_defaults[name]
    ]

    assert drift == []


def test_firewall_aliases_share_structure():
    options = load_yaml(ROLES_DIR / "firewall" / "meta" / "argument_specs.yml")["argument_specs"]["main"]["options"]

    for alias in ("firewall_global", "firewall_group", "firewall_host"):
        assert options[alias]["options"] == options["firewall_tables"]["options"]
