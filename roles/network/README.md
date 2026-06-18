# Ansible Role: network

Network configuration management for DNS resolution and network interface configuration.

## Features

- **DNS Configuration**: Manage system DNS resolver settings
- **Network Interfaces**: Configure network interface settings
- **systemd-resolved Integration**: Modern DNS management
- **Static and DHCP**: Support for both static and dynamic configuration
- **Multi-Interface**: Manage multiple network interfaces

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/network_role.html](https://guide.arillso.io/collections/arillso/system/network_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.network
        vars:
            network_dns_nameservers:
                - 1.1.1.1
                - 1.0.0.1
```

## Variables

| Variable                       | Default | Description                                |
| ------------------------------ | ------- | ------------------------------------------ |
| `network_resolv_enabled`       | `true`  | Manage DNS resolver configuration          |
| `network_netplan_enabled`      | `false` | Manage netplan interface configuration     |
| `network_dns_nameservers`      | `[]`    | DNS nameserver addresses                   |
| `network_dns_search`           | `[]`    | DNS search domains                         |
| `network_use_systemd_resolved` | `true`  | Use systemd-resolved for DNS               |
| `network_netplan_config`       | `{}`    | Netplan network definition (dict)          |
| `network_netplan_apply`        | `false` | Run `netplan apply` after rendering config |
| `network_validate_netplan`     | `true`  | Run `netplan generate` to validate config  |
| `network_backup_configs`       | `true`  | Back up config files before changes        |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/network_role.html) for detailed docs.

## Check Mode

This role is partially `--check` compatible. Config rendering is check-safe, but `netplan generate` (validation) and `netplan apply` are gated on a changed config file and are not executed/validated meaningfully in check mode.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
