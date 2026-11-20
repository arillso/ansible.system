"""
nftables filter plugins for YAML structure processing
Clean, maintainable conversion from YAML to nftables syntax
Hierarchical merge: firewall_tables → firewall_global → firewall_group → firewall_host
"""

import json
import os


class FilterModule:
    """Ansible filter plugins for nftables YAML structure processing"""

    def filters(self):
        return {
            "to_nftables_hierarchy": self.merge_nftables_structure,
            "to_nftables_rule": self.rule_to_nft,
            "to_nftables_ports": self.format_port_list,
        }

    def _should_debug(self):
        """Check if debug output should be enabled"""
        # Simple environment variable check - most reliable approach
        return os.environ.get("NFTABLES_DEBUG", "").lower() in ["true", "1", "yes"]

    def _debug_print(self, message):
        """Print debug message only if debug mode is enabled"""
        if getattr(self, "_debug_enabled", False) or self._should_debug():
            print(f"[nftables_filter] {message}")

    LEVELS = ("firewall_tables", "firewall_global", "firewall_group", "firewall_host")
    BASE_CHAIN_KEYS = ("type", "hook", "priority", "policy")

    def merge_nftables_structure(self, firewall_configs, debug=False):
        """
        Merge the configuration levels in priority order:
        firewall_tables (base) -> firewall_global -> firewall_group -> firewall_host

        Tables match on (family, name), chains and sets on name. A later level
        overrides chain settings and sets, and appends its rules to the chain.
        `replace: true` on a table drops everything earlier levels defined for
        it. Rules marked `final: true` move to the end of their chain.
        """
        self._debug_enabled = debug or self._should_debug()

        if not firewall_configs or not isinstance(firewall_configs, dict):
            self._debug_print("ERROR: Expected dict with firewall configurations")
            return []

        merged = {}
        for level in self.LEVELS:
            for entry in self._validate_config(firewall_configs.get(level, []), level):
                table = entry["table"]
                key = (table["family"], table["name"])
                if key in merged and not table.pop("replace", False):
                    self._merge_table(merged[key], table)
                else:
                    table.pop("replace", None)
                    merged[key] = table

        result = []
        for table in merged.values():
            for chain in table["chains"]:
                if "hook" in chain:
                    chain.setdefault("type", "filter")
                    chain.setdefault("priority", 0)
                    chain.setdefault("policy", "accept")
                chain["rules"].sort(
                    key=lambda rule: bool(isinstance(rule, dict) and rule.get("final"))
                )
            # Regular chains first, so jump/goto targets precede their callers.
            table["chains"].sort(key=lambda chain: "hook" in chain)
            result.append({"table": table})

        if self._debug_enabled:
            self._debug_print(f"Final result: {json.dumps(result, indent=2, default=str)}")
        return result

    def _merge_table(self, base, override):
        """Merge one validated table into another in place."""
        sets = {s["name"]: s for s in base["sets"]}
        sets.update({s["name"]: s for s in override["sets"]})
        base["sets"] = list(sets.values())

        chains = {c["name"]: c for c in base["chains"]}
        for chain in override["chains"]:
            if chain["name"] not in chains:
                base["chains"].append(chain)
                continue
            target = chains[chain["name"]]
            for key in self.BASE_CHAIN_KEYS:
                if key in chain:
                    target[key] = chain[key]
            target["rules"].extend(chain["rules"])

    def _validate_config(self, config, config_name):
        """Validate and normalize a single configuration"""

        if not config:
            self._debug_print(f"{config_name} is empty")
            return []

        if not isinstance(config, list):
            self._debug_print(f"ERROR: {config_name} is not a list: {type(config)}")
            return []

        validated_tables = []

        for i, table_config in enumerate(config):
            self._debug_print(f"Validating {config_name}[{i}]: type={type(table_config)}")

            if not isinstance(table_config, dict):
                self._debug_print(
                    f"WARNING: {config_name}[{i}] is not a dict: {type(table_config)}"
                )
                continue

            if "table" not in table_config:
                self._debug_print(f"WARNING: {config_name}[{i}] missing 'table' key")
                continue

            table = table_config["table"]
            if not isinstance(table, dict):
                self._debug_print(f"WARNING: {config_name}[{i}].table is not a dict: {type(table)}")
                continue

            if "name" not in table or "family" not in table:
                self._debug_print(f"WARNING: {config_name}[{i}].table missing name/family")
                continue

            # Normalize chains
            chains = table.get("chains") or []
            if not isinstance(chains, list):
                self._debug_print(f"WARNING: {config_name}[{i}].table.chains is not a list")
                continue

            normalized_chains = []
            for j, chain in enumerate(chains):
                if not isinstance(chain, dict):
                    self._debug_print(f"WARNING: {config_name}[{i}].chains[{j}] is not a dict")
                    continue

                if "name" not in chain:
                    self._debug_print(f"WARNING: {config_name}[{i}].chains[{j}] missing name")
                    continue

                # Base-chain defaults are applied after merging, so an override
                # level only changes the keys it sets. Without a hook the chain
                # is a regular chain (jump/goto target).
                normalized_chain = {
                    k: chain[k] for k in ("name",) + self.BASE_CHAIN_KEYS if k in chain
                }
                rules = chain.get("rules") or []
                if not isinstance(rules, list):
                    self._debug_print(
                        f"WARNING: {config_name}[{i}].chains[{j}].rules is not a list"
                    )
                    rules = []
                normalized_chain["rules"] = list(rules)

                normalized_chains.append(normalized_chain)

            normalized_sets = []
            for set_def in table.get("sets") or []:
                if not isinstance(set_def, dict) or "name" not in set_def or "type" not in set_def:
                    self._debug_print(f"WARNING: {config_name}[{i}].sets entry needs name and type")
                    continue
                flags = set_def.get("flags") or []
                normalized_sets.append(
                    {
                        "name": set_def["name"],
                        "type": set_def["type"],
                        "flags": [flags] if isinstance(flags, str) else list(flags),
                        "elements": list(set_def.get("elements") or []),
                    }
                )

            normalized_table = {
                "table": {
                    "name": table["name"],
                    "family": table["family"],
                    "replace": bool(table.get("replace", False)),
                    "sets": normalized_sets,
                    "chains": normalized_chains,
                }
            }

            validated_tables.append(normalized_table)
            self._debug_print(
                f"Validated {config_name}[{i}]: {table['family']}.{table['name']} with {len(normalized_chains)} chains"
            )

        return validated_tables

    def rule_to_nft(self, rule_dict):  # noqa: C901
        """Convert YAML rule format to nftables syntax"""
        if not isinstance(rule_dict, dict):
            return str(rule_dict)

        rule_parts = []

        # Interface conditions
        if "iifname" in rule_dict:
            rule_parts.append(f'iifname "{rule_dict["iifname"]}"')
        if "oifname" in rule_dict:
            rule_parts.append(f'oifname "{rule_dict["oifname"]}"')

        # IP Protocol conditions
        if "ip_protocol" in rule_dict:
            rule_parts.append(f"ip protocol {rule_dict['ip_protocol']}")
        if "ip6_nexthdr" in rule_dict:
            rule_parts.append(f"ip6 nexthdr {rule_dict['ip6_nexthdr']}")

        # IPv4 Source/Destination addresses
        if "ip_saddr" in rule_dict:
            rule_parts.append(f"ip saddr {rule_dict['ip_saddr']}")
        if "ip_daddr" in rule_dict:
            rule_parts.append(f"ip daddr {rule_dict['ip_daddr']}")

        # IPv6 Source/Destination addresses
        if "ip6_saddr" in rule_dict:
            rule_parts.append(f"ip6 saddr {rule_dict['ip6_saddr']}")
        if "ip6_daddr" in rule_dict:
            rule_parts.append(f"ip6 daddr {rule_dict['ip6_daddr']}")

        # Set references for performance optimization
        if "ip_saddr_set" in rule_dict:
            rule_parts.append(f"ip saddr {rule_dict['ip_saddr_set']}")
        if "ip_daddr_set" in rule_dict:
            rule_parts.append(f"ip daddr {rule_dict['ip_daddr_set']}")
        if "ip6_saddr_set" in rule_dict:
            rule_parts.append(f"ip6 saddr {rule_dict['ip6_saddr_set']}")
        if "ip6_daddr_set" in rule_dict:
            rule_parts.append(f"ip6 daddr {rule_dict['ip6_daddr_set']}")

        # Port conditions - with enhanced formatting
        if "tcp_dport" in rule_dict:
            port_value = self.format_port_list(rule_dict["tcp_dport"])
            rule_parts.append(f"tcp dport {port_value}")
        if "tcp_sport" in rule_dict:
            port_value = self.format_port_list(rule_dict["tcp_sport"])
            rule_parts.append(f"tcp sport {port_value}")
        if "udp_dport" in rule_dict:
            port_value = self.format_port_list(rule_dict["udp_dport"])
            rule_parts.append(f"udp dport {port_value}")
        if "udp_sport" in rule_dict:
            port_value = self.format_port_list(rule_dict["udp_sport"])
            rule_parts.append(f"udp sport {port_value}")

        # Port set references for performance
        if "tcp_dport_set" in rule_dict:
            rule_parts.append(f"tcp dport {rule_dict['tcp_dport_set']}")
        if "tcp_sport_set" in rule_dict:
            rule_parts.append(f"tcp sport {rule_dict['tcp_sport_set']}")
        if "udp_dport_set" in rule_dict:
            rule_parts.append(f"udp dport {rule_dict['udp_dport_set']}")
        if "udp_sport_set" in rule_dict:
            rule_parts.append(f"udp sport {rule_dict['udp_sport_set']}")

        # Connection tracking (basic)
        if "ct_state" in rule_dict:
            states = rule_dict["ct_state"]
            if isinstance(states, list):
                rule_parts.append(f"ct state {','.join(states)}")
            else:
                rule_parts.append(f"ct state {states}")

        # Extended connection tracking
        if "ct_status" in rule_dict:
            rule_parts.append(f"ct status {rule_dict['ct_status']}")
        if "ct_mark" in rule_dict:
            rule_parts.append(f"ct mark {rule_dict['ct_mark']}")
        if "ct_direction" in rule_dict:
            rule_parts.append(f"ct direction {rule_dict['ct_direction']}")

        # ICMP handling
        if "icmp_type" in rule_dict:
            rule_parts.append(f"icmp type {rule_dict['icmp_type']}")
        if "icmp_code" in rule_dict:
            rule_parts.append(f"icmp code {rule_dict['icmp_code']}")
        if "icmpv6_type" in rule_dict:
            rule_parts.append(f"icmpv6 type {rule_dict['icmpv6_type']}")

        # Meta expressions
        if "meta_mark" in rule_dict:
            rule_parts.append(f"meta mark {rule_dict['meta_mark']}")
        if "meta_nfproto" in rule_dict:
            rule_parts.append(f"meta nfproto {rule_dict['meta_nfproto']}")
        if "meta_length" in rule_dict:
            rule_parts.append(f"meta length {rule_dict['meta_length']}")
        if "meta_protocol" in rule_dict:
            rule_parts.append(f"meta protocol {rule_dict['meta_protocol']}")

        # Rate limiting
        if "limit" in rule_dict:
            limit_rule = f"limit rate {rule_dict['limit']}"
            if "burst" in rule_dict:
                limit_rule += f" burst {rule_dict['burst']} packets"
            rule_parts.append(limit_rule)

        # Enhanced logging
        # An empty prefix switches logging off for the rule.
        if rule_dict.get("log_prefix"):
            log_parts = [f'log prefix "{rule_dict["log_prefix"]}"']

            if "log_level" in rule_dict:
                log_parts.append(f"level {rule_dict['log_level']}")
            if "log_group" in rule_dict:
                log_parts.append(f"group {rule_dict['log_group']}")
            if "log_snaplen" in rule_dict:
                log_parts.append(f"snaplen {rule_dict['log_snaplen']}")
            if "log_queue_threshold" in rule_dict:
                log_parts.append(f"queue-threshold {rule_dict['log_queue_threshold']}")

            rule_parts.append(" ".join(log_parts))

        # Enhanced actions and verdicts
        action = rule_dict.get("action", "accept")

        if action == "dnat" and "to" in rule_dict:
            rule_parts.append(f"dnat to {rule_dict['to']}")
        elif action == "masquerade":
            rule_parts.append("masquerade")
        elif action == "reject":
            if "reject_with" in rule_dict:
                rule_parts.append(f"reject with {self._reject_reason(rule_dict['reject_with'])}")
            else:
                rule_parts.append("reject")
        elif action == "queue":
            if "queue_num" in rule_dict:
                rule_parts.append(f"queue num {rule_dict['queue_num']}")
            else:
                rule_parts.append("queue")
        elif action == "jump" and "target_chain" in rule_dict:
            rule_parts.append(f"jump {rule_dict['target_chain']}")
        elif action == "goto" and "goto_chain" in rule_dict:
            rule_parts.append(f"goto {rule_dict['goto_chain']}")
        else:
            rule_parts.append(action)

        return " ".join(rule_parts)

    @staticmethod
    def _reject_reason(value):
        """Map `icmp-admin-prohibited` style values to nft `icmp type admin-prohibited`."""
        value = str(value)
        if value == "tcp-reset":
            return "tcp reset"
        proto, sep, code = value.partition("-")
        if " " not in value and sep and proto in ("icmp", "icmpv6", "icmpx"):
            return f"{proto} type {code}"
        return value  # already in nft syntax, e.g. "icmp type port-unreachable"

    def format_port_list(self, port_value):
        """Enhanced port formatting for nftables syntax"""
        if isinstance(port_value, list):
            if len(port_value) == 1:
                return str(port_value[0])
            else:
                return "{ " + ", ".join(map(str, port_value)) + " }"
        elif isinstance(port_value, str):
            # Handle port ranges and service names
            if "-" in port_value and not port_value.startswith("{"):
                # Check if it's a numeric port range like "1000-2000"
                range_parts = port_value.split("-")
                if len(range_parts) == 2 and all(part.strip().isdigit() for part in range_parts):
                    return port_value  # It's a valid port range
                else:
                    return port_value  # It's a service name or other string
            elif port_value.startswith("{") and port_value.endswith("}"):
                # Already formatted as set
                return port_value
            else:
                # Service name or single port
                return port_value
        elif isinstance(port_value, int):
            return str(port_value)
        else:
            return str(port_value)
