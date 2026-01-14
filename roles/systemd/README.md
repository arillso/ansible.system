# Ansible Role: systemd

Comprehensive systemd management for services, unit files, and journald configuration.

## Features

- **Service Management**: Start, stop, enable, and disable services
- **Unit File Deployment**: Deploy custom systemd unit files
- **Journald Configuration**: Configure systemd journal settings
- **Timer Management**: Create and manage systemd timers
- **Multi-Entry-Point Support**: Flexible task organization

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/systemd_role.html](https://guide.arillso.io/collections/arillso/system/systemd_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.systemd
        vars:
            systemd_services:
                - name: docker
                  state: started
                  enabled: true
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
