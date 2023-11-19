# arillso.system.apt_cache

This Ansible role is designed for updating the APT package cache. It ensures that the cache is up-to-date and not expired.

## Requirements

- **Ansible Version**: 2.15 or higher
- **Access**: Adequate permissions to update the APT package cache on target systems

## Role Variables

Variables for customizing the APT cache update are defined in `defaults/main.yml`. Users can override these in their playbook. Key variables include:

### APT Cache Configuration

- `apt_cache_valid_time`: The maximum age (in seconds) of the package cache before it is considered stale and needs to be updated (default: 86400).
- `apt_cache_update_cache_retries`: The maximum number of attempts to retry updating the cache if it fails (default: 5).
- `apt_cache_update_cache_retry_max_delay`: The maximum delay (in seconds) between retry attempts when updating the cache (default: 12).
- `apt_cache_force_apt_get`: Whether to force the use of apt-get instead of apt when updating the cache (default: true).

## Documentation

For detailed information and advanced usage, please refer to our guide:

[Arillso System Guide](https://guide.arillso.io/collections/arillso/system/apt_cache_role.html#ansible-collections-arillso-system-apt-cache-role)

## Dependencies

This role is standalone and does not require other Ansible roles as dependencies.

## Example Playbook

Example playbook for using `arillso.system.apt_cache`:

```yaml
- hosts: all
  become: yes
  roles:
    - arillso.system.apt_cache
  vars:
    apt_cache_valid_time: 72000
    apt_cache_update_cache_retries: 3
    apt_cache_update_cache_retry_max_delay: 10
    apt_cache_force_apt_get: false
```
