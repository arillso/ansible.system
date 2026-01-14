# Ansible Role: ansible

Configures Ansible automation with systemd timers for self-managing infrastructure.

## Features

- **Ansible Pull Mode**: Repository-first configuration with git integration
- **Local Playbook Mode**: Execute local playbooks on schedule
- **Systemd Timers**: Flexible scheduling with systemd calendar syntax
- **Self-Healing**: Automatic configuration drift correction
- **Logging**: Comprehensive logging with rotation

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/ansible_role.html](https://guide.arillso.io/collections/arillso/system/ansible_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.ansible
        vars:
            ansible_mode: pull
            ansible_pull_url: https://github.com/myorg/infra.git
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
