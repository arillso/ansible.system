# Ansible Role: ready

Waits for system readiness before configuration, ensuring SSH connectivity and cloud-init completion.

## Features

- **SSH Connectivity Check**: Wait for SSH to be available
- **Cloud-Init Completion**: Ensure cloud-init has finished
- **Configurable Timeout**: Set custom wait timeouts
- **Automatic Retry**: Built-in retry logic with backoff
- **Error Recovery**: Graceful handling of temporary failures

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/ready_role.html](https://guide.arillso.io/collections/arillso/system/ready_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.ready
        vars:
            ready_timeout: 300
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
