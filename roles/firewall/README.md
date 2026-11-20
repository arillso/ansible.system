# Ansible Role: firewall

Modern YAML-driven nftables firewall management with hierarchical configuration merging.

## Features

- **YAML-Driven Configuration**: Intuitive YAML to nftables mapping
- **Hierarchical Merging**: Global → Group → Host configuration inheritance
- **Validation**: the rendered file is checked with `nft -c` before it is installed
- **Systemd Integration**: Enhanced dependency management
- **IPv4/IPv6 Dual-Stack**: Native support for inet family tables

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/firewall_role.html](https://guide.arillso.io/collections/arillso/system/firewall_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.firewall
        vars:
            firewall_tables:
                - table:
                      name: filter
                      family: inet
```

## Variables

| Variable                       | Default                            | Description                                                                                                                                                                                                                                           |
| ------------------------------ | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `firewall_tables`              | `[{...}]`                          | Base nftables ruleset: an `inet filter` table with input/forward (policy `drop`) and output (policy `accept`) chains; input accepts loopback, established/related, ICMPv6 neighbor discovery and new SSH connections, then logs what the policy drops |
| `firewall_ssh_port`            | `access_ssh_port` or `22`          | TCP port the default input chain accepts SSH on                                                                                                                                                                                                       |
| `firewall_ssh_rate_limit`      | `10/minute`                        | Rate limit for **new** SSH connections. Established sessions match the preceding established/related rule and are never throttled                                                                                                                     |
| `firewall_ssh_rate_burst`      | `5`                                | Burst allowance in packets on top of the SSH rate limit                                                                                                                                                                                               |
| `firewall_log_drop_rate_limit` | `5/minute`                         | Rate limit for the log-on-drop rule; caps log volume independently of traffic                                                                                                                                                                         |
| `firewall_log_drop_prefix`     | `nft-drop-input:` + trailing space | Log prefix for packets dropped by the input chain policy; `""` switches the log off. Keep the trailing space — nftables appends the details after it                                                                                                  |
| `firewall_global`              | `[]`                               | Global-level rules merged on top of the base                                                                                                                                                                                                          |
| `firewall_group`               | `[]`                               | Group-level rules merged on top of global                                                                                                                                                                                                             |
| `firewall_host`                | `[]`                               | Host-level rules merged last (highest precedence)                                                                                                                                                                                                     |

## Merging

Tables match on `family` and `name`, chains and sets on `name`. A later level
sets the chain keys it names (`type`, `hook`, `priority`, `policy`), replaces
sets with the same name and appends its rules. Rules with `final: true` stay
last, which keeps the default log-and-drop rule behind added rules. Set
`replace: true` on a table to drop what earlier levels defined for it.

```yaml
firewall_host:
    - table:
          name: filter
          family: inet
          chains:
              - name: input
                rules:
                    - comment: "Accept HTTPS"
                      tcp_dport: 443
                      ct_state: ["new"]
                      action: accept
```

A chain without `hook` is a regular chain for `jump`/`goto`. Named sets go
under `sets` (`name`, `type`, optional `flags`, `elements`) and are referenced
as `@name`, e.g. `ip_saddr_set: "@trusted"`.

Tables removed from the YAML are deleted on the next run, and stopping the
service deletes the managed tables. Tables of other sources (Docker,
kube-proxy) are not touched.

Raise `firewall_ssh_rate_limit` on hosts that legitimately open many short-lived SSH connections (CI runners, bastions) rather than removing the rule.

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/firewall_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Configuration is rendered via templates and applied by idempotent modules; no command output is relied upon mid-play.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
