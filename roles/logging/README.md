# Ansible Role: logging

Comprehensive logging management for configuring logrotate and rsyslog.

## Features

- **Logrotate Configuration**: Manage log rotation policies
- **Rsyslog Management**: Configure rsyslog rules and forwarding
- **Remote Logging**: Forward logs to remote syslog servers
- **Custom Rules**: Support for custom rsyslog rules
- **Log Compression**: Automatic compression of rotated logs

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/logging_role.html](https://guide.arillso.io/collections/arillso/system/logging_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.logging
        vars:
            logging_logrotate_configs:
                - name: app
                  path: /var/log/app/*.log
                  rotate: 14
```

## Variables

| Variable                         | Default              | Description                                  |
| -------------------------------- | -------------------- | -------------------------------------------- |
| `logging_logrotate_enabled`      | `true`               | Manage logrotate configuration               |
| `logging_rsyslog_enabled`        | `true`               | Manage rsyslog configuration                 |
| `logging_logrotate_entries`      | `[]`                 | Custom logrotate definitions (list of dicts) |
| `logging_logrotate_rotate`       | `4`                  | Default number of rotations to keep          |
| `logging_logrotate_compress`     | `true`               | Compress rotated logs                        |
| `logging_rsyslog_entries`        | `[]`                 | Custom rsyslog rule snippets (list of dicts) |
| `logging_rsyslog_remote_servers` | `[]`                 | Remote syslog forwarding targets             |
| `logging_rsyslog_modules`        | `[imuxsock, imklog]` | rsyslog input modules to load                |
| `logging_backup_configs`         | `true`               | Back up config files before changes          |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/logging_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fully supported; logrotate/rsyslog config is rendered with templates and services managed via idempotent modules.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
