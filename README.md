# Ansible Collection: arillso.system

[![license](https://img.shields.io/github/license/mashape/apistatus.svg?style=popout-square)](LICENSE) [![Ansible Galaxy](http://img.shields.io/badge/ansible--galaxy-arillso.system-blue.svg?style=popout-square)](https://galaxy.ansible.com/arillso/system)

## Description

This Ansible collection provides comprehensive system configuration and management capabilities for Linux servers. It includes unified roles for access control, package management, network configuration, firewall setup, logging, and system tuning.

## Roles

### Core System Roles

- **[access](roles/access)** - User/group/SSH/sudo management
- **[ansible](roles/ansible)** - Ansible automation with systemd timer
- **[facts](roles/facts)** - Extended system facts (cloud, container, security)
- **[packages](roles/packages)** - Package management with APT, DNF, unattended upgrades
- **[python](roles/python)** - Python and pip management
- **[ready](roles/ready)** - System readiness checks
- **[shell](roles/shell)** - Shell environment and MOTD configuration

### Infrastructure Roles

- **[firewall](roles/firewall)** - NFTables firewall configuration
- **[logging](roles/logging)** - Log management (rsyslog, logrotate)
- **[network](roles/network)** - Network configuration (netplan, resolv)
- **[systemd](roles/systemd)** - Systemd service/unit/journald management

### Advanced Roles

- **[bitwarden_secrets](roles/bitwarden_secrets)** - Bitwarden CLI secret management
- **[thermal](roles/thermal)** - CPU thermal management
- **[tuning](roles/tuning)** - System performance tuning (CPU, IO, network, swap)

## Plugins

### Lookup Plugins

- **environment_files** - Curate file lists based on patterns
- **github_latest_release** - Fetch latest GitHub release version

### Modules

- **apt_update_info** - Retrieve list of updatable APT packages
- **reboot_info** - Check if system requires reboot

### Filter Plugins

- **from_toml** - Convert TOML string to dictionary
- **to_toml** - Convert dictionary to TOML string
- **to_nice_toml** - Convert dictionary to nicely formatted TOML
- **to_nftables_hierarchy** - Generate nftables rule hierarchy
- **to_nftables_rule** - Generate nftables rule
- **to_nftables_ports** - Generate nftables port rules

## Installation

Install this collection from Ansible Galaxy:

```bash
ansible-galaxy collection install arillso.system
```

Or add it to your `requirements.yml`:

```yaml
---
collections:
    - name: arillso.system
      version: ">=1.0.0"
```

## Requirements

- Ansible >= 2.16
- Python >= 3.11

## Dependencies

- ansible.posix >= 2.0.0
- community.general >= 9.0.0
- community.crypto >= 2.0.0

## Documentation

Full documentation is available at:
<https://guide.arillso.io/collections/arillso/system/>

**Breaking Changes in 1.0.0:**

Version 1.0.0 introduces a major restructuring. Many roles have been removed and consolidated. See [CHANGELOG.md](CHANGELOG.md) for migration guidance.

## License

This project is under the MIT License. See the [LICENSE](LICENSE) file for the full license text.

## Copyright

(c) 2024-2026, Arillso
