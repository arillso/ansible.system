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

## Variables

| Variable                             | Default               | Description                                 |
| ------------------------------------ | --------------------- | ------------------------------------------- |
| `systemd_services`                   | `[]`                  | Services to manage (list of dicts)          |
| `systemd_units`                      | `[]`                  | Custom unit files to deploy (list of dicts) |
| `systemd_unit_path`                  | `/etc/systemd/system` | Directory for deployed unit files           |
| `systemd_journald_enabled`           | `true`                | Manage journald configuration               |
| `systemd_journald_storage`           | `auto`                | journald storage mode                       |
| `systemd_journald_system_max_use`    | `1G`                  | Max disk space for the journal              |
| `systemd_journald_max_retention_sec` | `1month`              | Max journal retention time                  |
| `systemd_daemon_reload`              | `false`               | Force `daemon-reload`                       |
| `systemd_validate_units`             | `true`                | Validate unit files before applying         |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/systemd_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fully supported; services, unit files, and journald config are handled by idempotent modules and templates.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
