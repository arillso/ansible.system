"""Unit tests for plugins/filter/nftables.py."""

from __future__ import annotations

import pytest
from ansible.errors import AnsibleFilterError
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

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("icmp-admin-prohibited", "reject with icmp type admin-prohibited"),
            ("icmpv6-no-route", "reject with icmpv6 type no-route"),
            ("icmpx-port-unreachable", "reject with icmpx type port-unreachable"),
            ("tcp-reset", "reject with tcp reset"),
        ],
    )
    def test_reject_with_choice_maps_to_nft_syntax(self, fm, value, expected):
        assert fm.rule_to_nft({"action": "reject", "reject_with": value}) == expected

    def test_empty_log_prefix_adds_no_log(self, fm):
        rule = {"limit": "5/minute", "log_prefix": "", "log_level": "info", "action": "drop"}
        assert fm.rule_to_nft(rule) == "limit rate 5/minute drop"

    def test_jump_with_target(self, fm):
        assert fm.rule_to_nft({"action": "jump", "target_chain": "ssh-acl"}) == "jump ssh-acl"

    def test_log_prefix_and_drop(self, fm):
        rule = {"log_prefix": "dropped:", "log_level": "warn", "action": "drop"}
        result = fm.rule_to_nft(rule)
        assert 'log prefix "dropped:"' in result
        assert "level warn" in result
        assert result.endswith("drop")

    def test_rate_limit_with_burst(self, fm):
        rule = {"limit": "10/minute", "burst": 5, "action": "accept"}
        assert fm.rule_to_nft(rule) == "limit rate 10/minute burst 5 packets accept"

    def test_rate_limit_without_burst(self, fm):
        assert fm.rule_to_nft({"limit": "5/second", "action": "drop"}) == "limit rate 5/second drop"

    def test_burst_from_jinja_renders_like_int(self, fm):
        # A default resolved through Jinja arrives as a string, so "5" and 5
        # have to produce the same rule — otherwise the shipped defaults would
        # render differently than this test suite exercises them.
        as_int = fm.rule_to_nft({"limit": "10/minute", "burst": 5, "action": "accept"})
        as_str = fm.rule_to_nft({"limit": "10/minute", "burst": "5", "action": "accept"})
        assert as_int == as_str

    def test_ssh_accept_matches_shipped_default(self, fm):
        # The default input chain rate-limits on ct_state new only: an
        # established session must not consume the connection budget.
        rule = {
            "tcp_dport": 22,
            "ct_state": ["new"],
            "limit": "10/minute",
            "burst": 5,
            "action": "accept",
        }
        assert fm.rule_to_nft(rule) == (
            "tcp dport 22 ct state new limit rate 10/minute burst 5 packets accept"
        )


class TestMergeNftablesStructure:
    def _base(self) -> dict:
        return {
            "firewall_tables": [
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
        assert result[0]["table"]["sets"] == []
        # Without a hook the chain stays a regular chain: no base-chain defaults.
        assert result[0]["table"]["chains"][0] == {"name": "input", "rules": [{"action": "accept"}]}

    def test_base_chain_defaults(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["chains"][0]["hook"] = "input"
        chain = fm.merge_nftables_structure(cfg)[0]["table"]["chains"][0]
        assert (chain["type"], chain["priority"], chain["policy"]) == ("filter", 0, "accept")

    def test_host_rules_append_to_base_chain(self, fm):
        cfg = self._base()
        base_chain = cfg["firewall_tables"][0]["table"]["chains"][0]
        base_chain.update(hook="input", policy="drop")
        base_chain["rules"] = [
            {"tcp_dport": 22, "action": "accept"},
            {"log_prefix": "drop: ", "action": "drop", "order": 1000},
        ]
        cfg["firewall_host"] = [
            {
                "table": {
                    "name": "filter",
                    "family": "inet",
                    "chains": [{"name": "input", "rules": [{"tcp_dport": 443}]}],
                },
            },
        ]
        result = fm.merge_nftables_structure(cfg)
        assert len(result) == 1
        chain = result[0]["table"]["chains"][0]
        assert chain["policy"] == "drop"  # not reset by the host level
        assert [r.get("tcp_dport") for r in chain["rules"]] == [22, 443, None]
        # Input lists stay untouched.
        assert len(base_chain["rules"]) == 2

    def test_override_changes_chain_settings(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["chains"][0]["hook"] = "input"
        cfg["firewall_group"] = [
            {
                "table": {
                    "name": "filter",
                    "family": "inet",
                    "chains": [{"name": "input", "policy": "drop"}],
                }
            },
        ]
        chain = fm.merge_nftables_structure(cfg)[0]["table"]["chains"][0]
        assert chain["policy"] == "drop"

    def test_replace_drops_earlier_levels(self, fm):
        cfg = self._base()
        cfg["firewall_host"] = [
            {"table": {"name": "filter", "family": "inet", "replace": True, "chains": []}},
        ]
        result = fm.merge_nftables_structure(cfg)
        assert result[0]["table"]["chains"] == []
        assert "replace" not in result[0]["table"]

    def test_distinct_tables_are_kept(self, fm):
        cfg = self._base()
        cfg["firewall_host"] = [{"table": {"name": "nat", "family": "ip", "chains": []}}]
        names = [t["table"]["name"] for t in fm.merge_nftables_structure(cfg)]
        assert names == ["filter", "nat"]

    def test_regular_chains_come_first(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["chains"] = [
            {
                "name": "input",
                "hook": "input",
                "rules": [{"action": "jump", "target_chain": "web"}],
            },
            {"name": "web", "rules": []},
        ]
        chains = fm.merge_nftables_structure(cfg)[0]["table"]["chains"]
        assert [c["name"] for c in chains] == ["web", "input"]

    def test_sets_are_normalized_and_overridden(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["sets"] = [
            {
                "name": "trusted",
                "type": "ipv4_addr",
                "flags": "interval",
                "elements": ["10.0.0.0/8"],
            },
        ]
        cfg["firewall_host"] = [
            {
                "table": {
                    "name": "filter",
                    "family": "inet",
                    "sets": [{"name": "trusted", "type": "ipv4_addr", "elements": ["192.0.2.1"]}],
                },
            },
        ]
        sets = fm.merge_nftables_structure(cfg)[0]["table"]["sets"]
        assert sets == [
            {"name": "trusted", "type": "ipv4_addr", "flags": [], "elements": ["192.0.2.1"]}
        ]

    def test_string_false_does_not_replace(self, fm):
        cfg = self._base()
        cfg["firewall_host"] = [
            {"table": {"name": "filter", "family": "inet", "replace": "false", "chains": []}},
        ]
        chains = fm.merge_nftables_structure(cfg)[0]["table"]["chains"]
        assert [c["name"] for c in chains] == ["input"]

    def test_negative_order_puts_host_rule_before_inherited(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["chains"][0]["rules"] = [
            {"tcp_dport": 8080, "action": "drop"},
        ]
        cfg["firewall_host"] = [
            {
                "table": {
                    "name": "filter",
                    "family": "inet",
                    "chains": [
                        {
                            "name": "input",
                            "rules": [{"tcp_dport": 8080, "ip_saddr": "10.0.0.5", "order": "-10"}],
                        },
                    ],
                },
            },
        ]
        rules = fm.merge_nftables_structure(cfg)[0]["table"]["chains"][0]["rules"]
        assert [r.get("ip_saddr") for r in rules] == ["10.0.0.5", None]

    def test_policy_without_hook_fails(self, fm):
        cfg = self._base()
        cfg["firewall_tables"][0]["table"]["chains"][0]["policy"] = "drop"
        with pytest.raises(AnsibleFilterError, match="need a hook"):
            fm.merge_nftables_structure(cfg)

    def test_new_chain_twice_in_one_table_is_merged(self, fm):
        cfg = self._base()
        web = {"name": "web", "rules": [{"action": "accept"}]}
        cfg["firewall_host"] = [
            {"table": {"name": "filter", "family": "inet", "chains": [web, web]}},
        ]
        chains = fm.merge_nftables_structure(cfg)[0]["table"]["chains"]
        assert [c["name"] for c in chains] == ["input", "web"]
        assert len(chains[1]["rules"]) == 2

    def test_invalid_input_returns_empty(self, fm):
        assert fm.merge_nftables_structure("nope") == []
        assert fm.merge_nftables_structure(None) == []

    def test_missing_table_key_is_skipped(self, fm):
        cfg = {
            "firewall_tables": [{"not_a_table": True}],
            "firewall_global": [],
            "firewall_group": [],
            "firewall_host": [],
        }
        assert fm.merge_nftables_structure(cfg) == []

    def test_missing_name_is_skipped(self, fm):
        cfg = {
            "firewall_tables": [{"table": {"family": "inet"}}],
            "firewall_global": [],
            "firewall_group": [],
            "firewall_host": [],
        }
        assert fm.merge_nftables_structure(cfg) == []

    def test_missing_family_defaults_to_inet(self, fm):
        cfg = self._base()
        cfg["firewall_host"] = [
            {
                "table": {
                    "name": "filter",
                    "chains": [{"name": "input", "rules": [{"tcp_dport": 443}]}],
                }
            },
        ]
        result = fm.merge_nftables_structure(cfg)
        assert len(result) == 1
        assert result[0]["table"]["chains"][0]["rules"][-1] == {"tcp_dport": 443}


class TestFilterModuleRegistration:
    def test_all_filters_exposed(self, fm):
        filters = fm.filters()
        assert set(filters) == {
            "to_nftables_hierarchy",
            "to_nftables_rule",
            "to_nftables_ports",
        }
