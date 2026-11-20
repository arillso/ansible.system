# Ansible Role: ready

Waits until the host accepts an Ansible connection and cloud-init has finished,
then gathers facts.

## Features

- **Connection wait**: `wait_for_connection` with the inventory's connection
  settings (`ansible_host`, `ansible_port`, ProxyJump)
- **cloud-init**: `cloud-init status --wait`, skipped on hosts without
  `/run/cloud-init`; fails on cloud-init errors, accepts recoverable ones (rc 2)
- **Reboot handling**: if cloud-init reboots the host during the wait, the
  role waits for the connection again and repeats the check (one reboot)

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/ready_role.html](https://guide.arillso.io/collections/arillso/system/ready_role.html)**

## Quick Start

```yaml
- hosts: servers
  gather_facts: false # facts are gathered by the role once the host is ready
  roles:
      - role: arillso.system.ready
        vars:
            ready_ssh_timeout: 600
```

## Variables

| Variable                   | Default | Description                                         |
| -------------------------- | ------- | --------------------------------------------------- |
| `ready_ssh_delay`          | `10`    | Delay before the first connection attempt (seconds) |
| `ready_ssh_timeout`        | `300`   | Max time to wait for a connection (seconds)         |
| `ready_cloud_init_timeout` | `900`   | Max time for `cloud-init status --wait` (seconds)   |
| `ready_gather_facts`       | `true`  | Gather facts once the system is ready               |
| `ready_gather_subset`      | `[]`    | Fact subset to gather                               |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/ready_role.html) for detailed docs.

## Check Mode

`wait_for_connection` is skipped in `--check`. The cloud-init wait runs anyway
(`check_mode: false`, read-only), so `--check` still waits for cloud-init and
fails on its errors.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
