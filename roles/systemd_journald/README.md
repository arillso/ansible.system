# arillso.system.systemd_journald

This Ansible role is used for configuring and managing `systemd-journald`, the system service for collecting and storing log data on Linux systems.

## Requirements

- Ansible 2.9 or higher.
- Access to the target Linux system with privileges to modify `systemd-journald` configuration and restart the service.

## Role Variables

The role uses various variables to customize the behavior of `systemd-journald`. These variables are defined in the `defaults/main.yml` file.
Users can override these default values by setting the variables in their playbook.

### General Configuration

- `systemd_journald_compress`: Whether to compress journal data (default: `true`).
- `systemd_journald_storage`: Defines where journal data is stored (`persistent`, `volatile`, `auto`, or `none`, default: `auto`).
- `systemd_journald_sync_interval_sec`: Interval to synchronize journal data to disk (default: `5m`).

### Log Level and Rate Limiting

- `systemd_journald_max_level_store`: Maximum priority level of messages to be stored (default: `info`).
- `systemd_journald_rate_limit_interval`: Time interval for rate limiting (default: `30s`).
- `systemd_journald_rate_limit_burst`: Maximum number of messages within rate limit interval (default: `1000`).

### Runtime and System Journal Configuration

- `systemd_journald_runtime_max_files`: Maximum number of runtime journal files (default: `100`).
- `systemd_journald_system_max_use`: Maximum disk space for system journal files (default: `1G`).

### Service State

- `systemd_journald_service_enabled`: Whether the `systemd-journald` service should be enabled (default: `true`).
- `systemd_journald_service_state`: Desired state of the service (`started`, `stopped`, `restarted`, `reloaded`, default: `started`).

For a complete list of variables, see the `defaults/main.yml` file.

## Dependencies

No other Ansible roles are required as dependencies.

## Example Playbook

Below is an example playbook that uses the `arillso.system.systemd_journald` role to configure `systemd-journald`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.systemd_journald
  vars:
    systemd_journald_max_level_store: "debug"
    systemd_journald_system_max_use: "500M"
```
