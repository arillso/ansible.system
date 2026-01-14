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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
