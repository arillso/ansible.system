"""
nftables filter plugins for YAML structure processing
Clean, maintainable conversion from YAML to nftables syntax
Hierarchical override: firewall → firewall_global → firewall_group → firewall_host
"""

import json
import os


class FilterModule(object):
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

    def merge_nftables_structure(self, firewall_configs, debug=False):
        """
        Apply hierarchical override for nftables configurations
        Priority: firewall (base) → firewall_global → firewall_group → firewall_host
        Later configurations completely override earlier ones if they have content
        """

        # Set debug mode from parameter or environment
        self._debug_enabled = debug or self._should_debug()

        # Debug: Print the input structure only in debug mode
        if self._debug_enabled:
            try:
                self._debug_print(f"Input type: {type(firewall_configs)}")
                self._debug_print(
                    f"Input value: {json.dumps(firewall_configs, indent=2, default=str)}"
                )
            except Exception as e:
                self._debug_print(f"Cannot serialize input: {e}")
                self._debug_print(f"Input repr: {repr(firewall_configs)}")

        # Validate input
        if not firewall_configs or not isinstance(firewall_configs, dict):
            self._debug_print("ERROR: Expected dict with firewall configurations")
            return []

        # Extract configurations in priority order
        firewall = firewall_configs.get("firewall", [])
        firewall_global = firewall_configs.get("firewall_global", [])
        firewall_group = firewall_configs.get("firewall_group", [])
        firewall_host = firewall_configs.get("firewall_host", [])

        self._debug_print(
            f"firewall length: {len(firewall) if isinstance(firewall, list) else 'not a list'}"
        )
        self._debug_print(
            f"firewall_global length: {len(firewall_global) if isinstance(firewall_global, list) else 'not a list'}"
        )
        self._debug_print(
            f"firewall_group length: {len(firewall_group) if isinstance(firewall_group, list) else 'not a list'}"
        )
        self._debug_print(
            f"firewall_host length: {len(firewall_host) if isinstance(firewall_host, list) else 'not a list'}"
        )

        # Apply hierarchical override logic
        # Start with base configuration
        result = self._validate_config(firewall, "firewall")

        # Override with global if it has content
        if firewall_global and len(firewall_global) > 0:
            self._debug_print("Overriding with firewall_global")
            result = self._validate_config(firewall_global, "firewall_global")

        # Override with group if it has content
        if firewall_group and len(firewall_group) > 0:
            self._debug_print("Overriding with firewall_group")
            result = self._validate_config(firewall_group, "firewall_group")

        # Override with host if it has content
        if firewall_host and len(firewall_host) > 0:
            self._debug_print("Overriding with firewall_host")
            result = self._validate_config(firewall_host, "firewall_host")

        if self._debug_enabled:
            self._debug_print(
                f"Final result: {json.dumps(result, indent=2, default=str)}"
            )

        return result

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
            self._debug_print(
                f"Validating {config_name}[{i}]: type={type(table_config)}"
            )

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
                self._debug_print(
                    f"WARNING: {config_name}[{i}].table is not a dict: {type(table)}"
                )
                continue

            if "name" not in table or "family" not in table:
                self._debug_print(
                    f"WARNING: {config_name}[{i}].table missing name/family"
                )
                continue

            # Normalize chains
            chains = table.get("chains", [])
            if not isinstance(chains, list):
                self._debug_print(
                    f"WARNING: {config_name}[{i}].table.chains is not a list"
                )
                continue

            normalized_chains = []
            for j, chain in enumerate(chains):
                if not isinstance(chain, dict):
                    self._debug_print(
                        f"WARNING: {config_name}[{i}].chains[{j}] is not a dict"
                    )
                    continue

                if "name" not in chain:
                    self._debug_print(
                        f"WARNING: {config_name}[{i}].chains[{j}] missing name"
                    )
                    continue

                # Normalize chain with defaults
                normalized_chain = {
                    "name": chain["name"],
                    "type": chain.get("type", "filter"),
                    "hook": chain.get("hook", "input"),
                    "priority": chain.get("priority", 0),
                    "policy": chain.get("policy", "accept"),
                    "rules": chain.get("rules", []),
                }

                # Validate rules
                if not isinstance(normalized_chain["rules"], list):
                    self._debug_print(
                        f"WARNING: {config_name}[{i}].chains[{j}].rules is not a list"
                    )
                    normalized_chain["rules"] = []

                normalized_chains.append(normalized_chain)

            # Create normalized table
            normalized_table = {
                "table": {
                    "name": table["name"],
                    "family": table["family"],
                    "chains": normalized_chains,
                }
            }

            validated_tables.append(normalized_table)
            self._debug_print(
                f"Validated {config_name}[{i}]: {table['family']}.{table['name']} with {len(normalized_chains)} chains"
            )

        return validated_tables

    def rule_to_nft(self, rule_dict):
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
            rule_parts.append(f'ip protocol {rule_dict["ip_protocol"]}')
        if "ip6_nexthdr" in rule_dict:
            rule_parts.append(f'ip6 nexthdr {rule_dict["ip6_nexthdr"]}')

        # IPv4 Source/Destination addresses
        if "ip_saddr" in rule_dict:
            rule_parts.append(f'ip saddr {rule_dict["ip_saddr"]}')
        if "ip_daddr" in rule_dict:
            rule_parts.append(f'ip daddr {rule_dict["ip_daddr"]}')

        # IPv6 Source/Destination addresses
        if "ip6_saddr" in rule_dict:
            rule_parts.append(f'ip6 saddr {rule_dict["ip6_saddr"]}')
        if "ip6_daddr" in rule_dict:
            rule_parts.append(f'ip6 daddr {rule_dict["ip6_daddr"]}')

        # Set references for performance optimization
        if "ip_saddr_set" in rule_dict:
            rule_parts.append(f'ip saddr {rule_dict["ip_saddr_set"]}')
        if "ip_daddr_set" in rule_dict:
            rule_parts.append(f'ip daddr {rule_dict["ip_daddr_set"]}')
        if "ip6_saddr_set" in rule_dict:
            rule_parts.append(f'ip6 saddr {rule_dict["ip6_saddr_set"]}')
        if "ip6_daddr_set" in rule_dict:
            rule_parts.append(f'ip6 daddr {rule_dict["ip6_daddr_set"]}')

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
            rule_parts.append(f'tcp dport {rule_dict["tcp_dport_set"]}')
        if "tcp_sport_set" in rule_dict:
            rule_parts.append(f'tcp sport {rule_dict["tcp_sport_set"]}')
        if "udp_dport_set" in rule_dict:
            rule_parts.append(f'udp dport {rule_dict["udp_dport_set"]}')
        if "udp_sport_set" in rule_dict:
            rule_parts.append(f'udp sport {rule_dict["udp_sport_set"]}')

        # Connection tracking (basic)
        if "ct_state" in rule_dict:
            states = rule_dict["ct_state"]
            if isinstance(states, list):
                rule_parts.append(f'ct state {",".join(states)}')
            else:
                rule_parts.append(f"ct state {states}")

        # Extended connection tracking
        if "ct_status" in rule_dict:
            rule_parts.append(f'ct status {rule_dict["ct_status"]}')
        if "ct_mark" in rule_dict:
            rule_parts.append(f'ct mark {rule_dict["ct_mark"]}')
        if "ct_direction" in rule_dict:
            rule_parts.append(f'ct direction {rule_dict["ct_direction"]}')

        # ICMP handling
        if "icmp_type" in rule_dict:
            rule_parts.append(f'icmp type {rule_dict["icmp_type"]}')
        if "icmp_code" in rule_dict:
            rule_parts.append(f'icmp code {rule_dict["icmp_code"]}')
        if "icmpv6_type" in rule_dict:
            rule_parts.append(f'icmpv6 type {rule_dict["icmpv6_type"]}')

        # Meta expressions
        if "meta_mark" in rule_dict:
            rule_parts.append(f'meta mark {rule_dict["meta_mark"]}')
        if "meta_nfproto" in rule_dict:
            rule_parts.append(f'meta nfproto {rule_dict["meta_nfproto"]}')
        if "meta_length" in rule_dict:
            rule_parts.append(f'meta length {rule_dict["meta_length"]}')
        if "meta_protocol" in rule_dict:
            rule_parts.append(f'meta protocol {rule_dict["meta_protocol"]}')

        # Rate limiting
        if "limit" in rule_dict:
            limit_rule = f'limit rate {rule_dict["limit"]}'
            if "burst" in rule_dict:
                limit_rule += f' burst {rule_dict["burst"]} packets'
            rule_parts.append(limit_rule)

        # Enhanced logging
        if "log_prefix" in rule_dict:
            log_parts = [f'log prefix "{rule_dict["log_prefix"]}"']

            if "log_level" in rule_dict:
                log_parts.append(f'level {rule_dict["log_level"]}')
            if "log_group" in rule_dict:
                log_parts.append(f'group {rule_dict["log_group"]}')
            if "log_snaplen" in rule_dict:
                log_parts.append(f'snaplen {rule_dict["log_snaplen"]}')
            if "log_queue_threshold" in rule_dict:
                log_parts.append(f'queue-threshold {rule_dict["log_queue_threshold"]}')

            rule_parts.append(" ".join(log_parts))

        # Enhanced actions and verdicts
        action = rule_dict.get("action", "accept")

        if action == "dnat" and "to" in rule_dict:
            rule_parts.append(f'dnat to {rule_dict["to"]}')
        elif action == "masquerade":
            rule_parts.append("masquerade")
        elif action == "reject":
            if "reject_with" in rule_dict:
                rule_parts.append(f'reject with {rule_dict["reject_with"]}')
            else:
                rule_parts.append("reject")
        elif action == "queue":
            if "queue_num" in rule_dict:
                rule_parts.append(f'queue num {rule_dict["queue_num"]}')
            else:
                rule_parts.append("queue")
        elif action == "jump" and "target_chain" in rule_dict:
            rule_parts.append(f'jump {rule_dict["target_chain"]}')
        elif action == "goto" and "goto_chain" in rule_dict:
            rule_parts.append(f'goto {rule_dict["goto_chain"]}')
        else:
            rule_parts.append(action)

        return " ".join(rule_parts)

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
                if len(range_parts) == 2 and all(
                    part.strip().isdigit() for part in range_parts
                ):
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
