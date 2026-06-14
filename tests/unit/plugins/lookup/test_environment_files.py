"""Unit tests for plugins/lookup/environment_files.py."""

from __future__ import annotations

import pytest
from ansible.errors import AnsibleError
from ansible_collections.arillso.system.plugins.lookup.environment_files import LookupModule


@pytest.fixture
def lookup() -> LookupModule:
    return LookupModule()


def test_short_syntax_resolves_pattern(lookup):
    patterns = {"alpha": {"file": "/etc/alpha.env", "owner": "root"}}
    result = lookup.run([["alpha"], patterns])
    assert result == [{"file": "/etc/alpha.env", "owner": "root", "export": False}]


def test_dict_syntax_overrides_default_export(lookup):
    files = [{"file": "/etc/foo.env", "export": True}]
    result = lookup.run([files, {}])
    assert result == [{"file": "/etc/foo.env", "export": True}]


def test_short_syntax_unknown_pattern_raises(lookup):
    with pytest.raises(AnsibleError, match="is not a valid pattern"):
        lookup.run([["does-not-exist"], {}])


def test_dict_syntax_missing_file_key_raises(lookup):
    with pytest.raises(AnsibleError, match='Missing "file" key'):
        lookup.run([[{"owner": "root"}], {}])


def test_non_string_non_dict_raises(lookup):
    with pytest.raises(AnsibleError, match="Expected a dict"):
        lookup.run([[42], {}])


def test_duplicate_file_is_overwritten_not_appended(lookup):
    files = [
        {"file": "/etc/dup.env", "owner": "root"},
        {"file": "/etc/dup.env", "owner": "deploy"},
    ]
    result = lookup.run([files, {}])
    assert result == [{"file": "/etc/dup.env", "owner": "deploy", "export": False}]
