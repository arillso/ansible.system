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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
