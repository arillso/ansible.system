"""Unit tests for plugins/filter/nftables.py."""

from __future__ import annotations

import pytest

from ansible_collections.arillso.system.plugins.filter.nftables import FilterModule


@pytest.fixture
def fm() -> FilterModule:
    return FilterModule()


class TestFormatPortList:
    def test_single_int(self, fm):
        assert fm.format_port_list(22) == "22"

    def test_list_with_single_entry(self, fm):
        assert fm.format_port_list([22]) == "22"

    def test_list_with_multiple_entries(self, fm):
        assert fm.format_port_list([22, 80, 443]) == "{ 22, 80, 443 }"

    def test_numeric_range_string(self, fm):
        assert fm.format_port_list("1000-2000") == "1000-2000"

    def test_already_set_formatted_string(self, fm):
        assert fm.format_port_list("{ 22, 80 }") == "{ 22, 80 }"

    def test_service_name_string(self, fm):
        assert fm.format_port_list("http") == "http"


class TestRuleToNft:
    def test_plain_action_only(self, fm):
        assert fm.rule_to_nft({"action": "accept"}) == "accept"

    def test_tcp_dport_and_accept(self, fm):
        assert fm.rule_to_nft({"tcp_dport": 22, "action": "accept"}) == "tcp dport 22 accept"

    def test_iifname_loopback(self, fm):
        rule = {"iifname": "lo", "action": "accept"}
        assert fm.rule_to_nft(rule) == 'iifname "lo" accept'

    def test_ct_state_list_renders_comma_join(self, fm):
        rule = {"ct_state": ["established", "related"], "action": "accept"}
        assert fm.rule_to_nft(rule) == "ct state established,related accept"

    def test_reject_with_message(self, fm):
        rule = {"action": "reject", "reject_with": "icmp port-unreachable"}
        assert fm.rule_to_nft(rule) == "reject with icmp port-unreachable"

    def test_jump_with_target(self, fm):
        assert fm.rule_to_nft({"action": "jump", "target_chain": "ssh-acl"}) == "jump ssh-acl"

    def test_log_prefix_and_drop(self, fm):
        rule = {"log_prefix": "dropped:", "log_level": "warn", "action": "drop"}
        result = fm.rule_to_nft(rule)
        assert 'log prefix "dropped:"' in result
        assert "level warn" in result
        assert result.endswith("drop")


class TestMergeNftablesStructure:
    def _base(self) -> dict:
        return {
            "firewall": [
                {
                    "table": {
                        "name": "filter",
                        "family": "inet",
                        "chains": [
                            {
                                "name": "input",
                                "rules": [{"action": "accept"}],
                            },
                        ],
                    },
                },
            ],
            "firewall_global": [],
            "firewall_group": [],
            "firewall_host": [],
        }

    def test_base_only(self, fm):
        result = fm.merge_nftables_structure(self._base())
        assert len(result) == 1
        assert result[0]["table"]["name"] == "filter"
        # Chain defaults are applied during validation.
        chain = result[0]["table"]["chains"][0]
        assert chain["type"] == "filter"
        assert chain["hook"] == "input"
        assert chain["policy"] == "accept"
        assert chain["priority"] == 0

    def test_host_overrides_global(self, fm):
        cfg = self._base()
        cfg["firewall_global"] = [
            {"table": {"name": "global-table", "family": "inet", "chains": []}},
        ]
        cfg["firewall_host"] = [
            {"table": {"name": "host-table", "family": "inet", "chains": []}},
        ]
        result = fm.merge_nftables_structure(cfg)
        assert result[0]["table"]["name"] == "host-table"

    def test_invalid_input_returns_empty(self, fm):
        assert fm.merge_nftables_structure("nope") == []
        assert fm.merge_nftables_structure(None) == []

    def test_missing_table_key_is_skipped(self, fm):
        cfg = {"firewall": [{"not_a_table": True}], "firewall_global": [],
               "firewall_group": [], "firewall_host": []}
        assert fm.merge_nftables_structure(cfg) == []

    def test_missing_name_or_family_is_skipped(self, fm):
        cfg = {
            "firewall": [{"table": {"name": "filter"}}],
            "firewall_global": [],
            "firewall_group": [],
            "firewall_host": [],
        }
        assert fm.merge_nftables_structure(cfg) == []


class TestFilterModuleRegistration:
    def test_all_filters_exposed(self, fm):
        filters = fm.filters()
        assert set(filters) == {
            "to_nftables_hierarchy",
            "to_nftables_rule",
            "to_nftables_ports",
        }
