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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
