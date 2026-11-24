"""Every role entry point carries a usable ``examples`` block in argument_specs.

antsibull-docs renders ``examples`` as the Examples section of a role page and
expects a string. An example that sets variables the entry point does not
declare is silently ignored by Ansible, and one that leaves out a required
option fails argument validation, so both are checked here.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

ROLES_DIR = Path(__file__).resolve().parents[2] / "roles"


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


ENTRY_POINTS = [
    (spec_file.parent.parent.name, entry, spec)
    for spec_file in sorted(ROLES_DIR.glob("*/meta/argument_specs.yml"))
    for entry, spec in load_yaml(spec_file)["argument_specs"].items()
]


def example_vars(plays, role: str, entry: str) -> set[str]:
    """Collect the variables an example passes to ``arillso.system.<role>`` entry ``entry``."""
    fqcn = f"arillso.system.{role}"
    used: set[str] = set()
    for play in plays:
        if entry == "main":
            for item in play.get("roles") or []:
                if isinstance(item, dict) and item.get("role") == fqcn:
                    used |= set(item.get("vars") or {})
        for task in play.get("tasks") or []:
            include = task.get("ansible.builtin.include_role")
            if include and include.get("name") == fqcn and include.get("tasks_from", "main") == entry:
                used |= set(task.get("vars") or {})
    return used


@pytest.mark.parametrize(
    ("role", "entry", "spec"),
    ENTRY_POINTS,
    ids=[f"{role}-{entry}" for role, entry, _ in ENTRY_POINTS],
)
def test_entry_point_has_valid_example(role, entry, spec):
    examples = spec.get("examples")
    assert isinstance(examples, str), "examples must be a block string"

    plays = yaml.safe_load(examples)
    assert isinstance(plays, list) and plays, "examples must be a list of plays"
    assert all(isinstance(play, dict) and "hosts" in play for play in plays)

    options = spec.get("options") or {}
    used = example_vars(plays, role, entry)
    assert used, "example sets no variable of this entry point"
    assert used <= set(options), f"undeclared variables: {sorted(used - set(options))}"

    required = {name for name, option in options.items() if option.get("required")}
    assert required <= used, f"required options missing: {sorted(required - used)}"
