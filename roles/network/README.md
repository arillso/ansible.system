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
| `network_dns_nameservers`      | `[]`    | DNS nameserver addresses (both paths)      |
| `network_dns_search`           | `[]`    | DNS search domains (both paths)            |
| `network_use_systemd_resolved` | `true`  | Use systemd-resolved for DNS               |
| `network_resolved_dns`         | `[]`    | Overrides `network_dns_nameservers`        |
| `network_resolved_llmnr`       | `"no"`  | LLMNR in systemd-resolved                  |
| `network_netplan_config`       | `{}`    | Netplan network definition (dict)          |
| `network_netplan_apply`        | `false` | Run `netplan apply` after rendering config |
| `network_validate_netplan`     | `true`  | Run `netplan generate` to validate config  |
| `network_backup_configs`       | `true`  | Back up config files before changes        |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/network_role.html) for detailed docs.

## systemd-resolved

With `network_use_systemd_resolved: true` the role installs `systemd-resolved`
when it is missing (a separate package on Debian 12, Ubuntu 24.04, EL 9), links
`/etc/resolv.conf` to it, and, if NetworkManager is installed, sets
`dns=systemd-resolved` in `/etc/NetworkManager/conf.d/90-arillso-dns-resolved.conf`.

## Netplan

`netplan generate` validates the new file before it is written. `netplan apply`
runs only when the file changes in the same run; a file written while
`network_netplan_apply` was `false` needs a manual `netplan apply`.

## Check Mode

This role is partially `--check` compatible. Config rendering is check-safe, but
the netplan validation and `netplan apply` do not run in check mode.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
