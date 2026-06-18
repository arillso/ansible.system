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

## Variables

| Variable              | Default | Description                                    |
| --------------------- | ------- | ---------------------------------------------- |
| `ready_ssh_port`      | `22`    | Port to probe for SSH availability             |
| `ready_ssh_delay`     | `10`    | Initial delay before first SSH check (seconds) |
| `ready_ssh_timeout`   | `300`   | Max time to wait for SSH (seconds)             |
| `ready_check_retries` | `60`    | cloud-init completion check retries            |
| `ready_check_delay`   | `2`     | Delay between cloud-init checks (seconds)      |
| `ready_rescue_pause`  | `30`    | Pause on rescue/recovery path (seconds)        |
| `ready_gather_facts`  | `true`  | Gather facts once the system is ready          |
| `ready_gather_subset` | `[]`    | Fact subset to gather                          |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/ready_role.html) for detailed docs.

## Check Mode

This role is partially `--check` compatible. It waits for live SSH connectivity and cloud-init state, which cannot be meaningfully evaluated in check mode; it makes no changes but its readiness gating is effectively a no-op.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
