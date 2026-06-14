"""Unit tests for plugins/filter/toml.py."""

from __future__ import annotations

import pytest
from ansible.errors import AnsibleFilterError
from ansible_collections.arillso.system.plugins.filter.toml import (
    FilterModule,
    from_toml,
    to_nice_toml,
    to_toml,
)


class TestFromToml:
    def test_parses_simple_toml(self):
        result = from_toml('name = "molecule"\nport = 8080\n')
        assert result == {"name": "molecule", "port": 8080}

    def test_parses_nested_toml(self):
        toml = 'title = "x"\n[server]\nhost = "a"\nport = 1\n'
        result = from_toml(toml)
        assert result == {"title": "x", "server": {"host": "a", "port": 1}}

    def test_empty_string_returns_empty_dict(self):
        assert from_toml("") == {}

    def test_invalid_input_raises_filter_error(self):
        with pytest.raises(AnsibleFilterError, match="Error parsing TOML"):
            from_toml("name = ")

    def test_non_string_raises_filter_error(self):
        with pytest.raises(AnsibleFilterError, match="requires a string"):
            from_toml(42)


class TestToToml:
    def test_serializes_simple_dict(self):
        result = to_toml({"name": "molecule", "port": 8080})
        assert "name" in result
        assert "molecule" in result
        assert "8080" in result

    def test_roundtrip(self):
        original = {"name": "x", "nested": {"key": "val", "n": 3}}
        assert from_toml(to_toml(original)) == original

    def test_non_dict_raises_filter_error(self):
        with pytest.raises(AnsibleFilterError, match="requires a dict"):
            to_toml("not a dict")


class TestToNiceToml:
    def test_renders_top_level_key_value(self):
        result = to_nice_toml({"key": "value"})
        assert 'key = "value"' in result

    def test_renders_nested_section_header(self):
        result = to_nice_toml({"server": {"host": "localhost", "port": 8080}})
        assert "[server]" in result
        assert 'host = "localhost"' in result
        assert "port = 8080" in result

    def test_renders_array_of_tables(self):
        result = to_nice_toml(
            {
                "products": [
                    {"name": "a", "price": 10},
                    {"name": "b", "price": 20},
                ],
            },
        )
        assert "[[products]]" in result
        assert result.count("[[products]]") == 2
        assert 'name = "a"' in result
        assert 'name = "b"' in result

    def test_boolean_lowercase(self):
        result = to_nice_toml({"flag_true": True, "flag_false": False})
        assert "flag_true = true" in result
        assert "flag_false = false" in result

    def test_list_of_scalars(self):
        result = to_nice_toml({"items": [1, 2, 3]})
        assert "items = [1, 2, 3]" in result

    def test_non_dict_raises_filter_error(self):
        with pytest.raises(AnsibleFilterError, match="requires a dict"):
            to_nice_toml(["not", "a", "dict"])


class TestFilterModuleRegistration:
    def test_filters_method_exposes_all_three(self):
        filters = FilterModule().filters()
        assert set(filters) == {"from_toml", "to_toml", "to_nice_toml"}
        assert filters["from_toml"] is from_toml
        assert filters["to_toml"] is to_toml
        assert filters["to_nice_toml"] is to_nice_toml
