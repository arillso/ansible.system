# Ansible Role: arillso.system.iptables

This Ansible role manages iptables rules for your system, enabling the creation, modification, and deletion of firewall rules.

## Requirements

- **Ansible Version**: 2.15 or higher is recommended.
- **Access**: Adequate permissions to modify environment variable files on the target systems.

## Role Variables

### `iptables_rule_action`

Specifies the action to perform on the rule (such as append, insert, delete). The default is `append`.

### `iptables_rule_chain`

Defines the iptables chain to modify (e.g., INPUT, FORWARD, OUTPUT). The default chain is `INPUT`.

### `iptables_rule_comment`

Optional comment associated with the rule. Default is not set.

### `iptables_rule_ctstate`

Connection tracking states to match (e.g., NEW, ESTABLISHED). Default is not set.

### `iptables_rule_destination`

Destination address or network to match. Default is not set.

### `iptables_rule_destination_port`

Single destination port to match. Default is not set.

### `iptables_rule_destination_ports`

Range or multiple destination ports to match. Default is not set.

### `iptables_rule_dst_range`

Destination address range to match. Default is not set.

### `iptables_rule_flush`

Option to flush rules in the specified chain. Default is not set.

### `iptables_rule_fragment`

Option to match fragmented packets. Default is not set.

### `iptables_rule_gateway`

Gateway to use for redirected packets. Default is not set.

### `iptables_rule_gid_owner`

Group ID to match for ownership. Default is not set.

### `iptables_rule_goto`

Target chain to jump to for 'GOTO' action. Default is not set.

### `iptables_rule_icmp_type`

ICMP type to match. Default is not set.

### `iptables_rule_in_interface`

Incoming interface to match (e.g., eth0). Default is not set.

### `iptables_rule_ip_version`

IP version to use (ipv4, ipv6). Default is not set.

### `iptables_rule_jump`

Target chain to jump to for 'JUMP' action. Default is not set.

### `iptables_rule_limit`

Rate limit matching for a rule. Default is not set.

### `iptables_rule_limit_burst`

Maximum burst rate allowed before the limit rule applies. Default is not set.

### `iptables_rule_log_level`

Log level for logging rule matches. Default is not set.

### `iptables_rule_log_prefix`

Prefix for log messages. Default is not set.

### `iptables_rule_match`

Match criteria for the rule. Default is not set.

### `iptables_rule_match_set`

Match set for 'ipset' match. Default is not set.

### `iptables_rule_match_set_flags`

Flags for the 'ipset' match. Default is not set.

### `iptables_rule_numeric`

Skip DNS-lookup if 'TRUE'. Default is not set.

### `iptables_rule_out_interface`

Outgoing interface to match (e.g., eth1). Default is not set.

### `iptables_rule_policy`

Policy to set on the chain (e.g., ACCEPT, DROP). Default is not set.

### `iptables_rule_protocol`

Network protocol to match (e.g., tcp, udp, icmp). Default is not set.

### `iptables_rule_reject_with`

Option for rejecting packets. Default is not set.

### `iptables_rule_rule_num`

Rule number to insert/delete a specific rule. Default is not set.

### `iptables_rule_set_counters`

Set packet and byte counters for a rule. Default is not set.

### `iptables_rule_set_dscp_mark`

Set DSCP mark in the IP header. Default is not set.

### `iptables_rule_set_dscp_mark_class`

Set DSCP class in the IP header. Default is not set.

### `iptables_rule_source`

Source address or network to match. Default is not set.

### `iptables_rule_source_port`

Single source port to match. Default is not set.

### `iptables_rule_src_range`

Source address range to match. Default is not set.

### `iptables_rule_state`

State of the rule (e.g., present, absent). Default is `present`.

### `iptables_rule_syn`

Option to match SYN packets. Default is not set.

### `iptables_rule_table`

Table to apply the rule (e.g., filter, nat). Default is `filter`.

### `iptables_rule_tcp_flags`

TCP flags to match. Default is not set.

### `iptables_rule_flags`

Custom flags to match. Default is not set.

### `iptables_rule_flags_set`

Set of flags to match. Default is not set.

### `iptables_rule_to_destination`

Target IP address for DNAT/SNAT. Default is not set.

### `iptables_rule_to_ports`

Target port(s) for DNAT/SNAT. Default is not set.

### `iptables_rule_to_source`

Source IP address for SNAT. Default is not set.

### `iptables_rule_uid_owner`

User ID to match for ownership. Default is not set.

### `iptables_rule_wait`

Wait time for xtables lock. Default is not set.

### `iptables_rules`

A list of iptables rules to be managed. Each item in the list is a dictionary specifying parameters of a rule. Default is an empty list.
