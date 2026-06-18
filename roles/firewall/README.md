# Ansible Role: firewall

Modern YAML-driven nftables firewall management with hierarchical configuration merging.

## Features

- **YAML-Driven Configuration**: Intuitive YAML to nftables mapping
- **Hierarchical Merging**: Global → Group → Host configuration inheritance
- **Automatic Validation**: Built-in configuration validation
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
            nftables:
                - table:
                      name: filter
                      family: inet
```

## Variables

| Variable          | Default   | Description                                                                                                                                                                                 |
| ----------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `firewall`        | `[{...}]` | Base nftables ruleset: an `inet filter` table with input/forward (policy `drop`) and output (policy `accept`) chains; input accepts loopback, established/related, and SSH (`tcp_dport 22`) |
| `firewall_global` | `[]`      | Global-level rules merged on top of the base                                                                                                                                                |
| `firewall_group`  | `[]`      | Group-level rules merged on top of global                                                                                                                                                   |
| `firewall_host`   | `[]`      | Host-level rules merged last (highest precedence)                                                                                                                                           |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/firewall_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Configuration is rendered via templates and applied by idempotent modules; no command output is relied upon mid-play.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
