# Ansible Role: packages

Manages system packages including installation, removal, repositories, keys, and APT configuration.

## Features

- **Package Management**: Install, update, and remove packages
- **Repository Management**: Configure APT repositories
- **GPG Key Management**: Manage repository signing keys
- **Cache Management**: Control APT cache updates
- **Upgrade Support**: System package upgrades
- **Unattended Upgrades**: Automatic security updates configuration

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/packages_role.html](https://guide.arillso.io/collections/arillso/system/packages_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.packages
        vars:
            packages_list:
                - name: git
                  state: present
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
