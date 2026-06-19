# Ansible Role: packages

Manages system packages including installation, removal, repositories, keys, and APT configuration.

## Features

- **Package Management**: Install, update, and remove packages
- **Repository Management**: Configure APT repositories
- **GPG Key Management**: Manage repository signing keys
- **Cache Management**: Control APT cache updates
- **Upgrade Support**: System package upgrades
- **Unattended Upgrades**: Automatic security updates configuration

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/packages_role.html](https://guide.arillso.io/collections/arillso/system/packages_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.packages
        vars:
            packages_list:
                - name: git
                  state: present
```

## Variables

| Variable                               | Default | Description                                |
| -------------------------------------- | ------- | ------------------------------------------ |
| `packages_list`                        | `[]`    | Packages to install/remove (list of dicts) |
| `packages_repositories`                | `[]`    | APT repositories to configure              |
| `packages_keys`                        | `[]`    | Repository GPG signing keys                |
| `packages_update_cache`                | `true`  | Update APT cache before operations         |
| `packages_cache_valid_time`            | `3600`  | APT cache validity in seconds              |
| `packages_upgrade`                     | `false` | Perform a system package upgrade           |
| `packages_autoremove`                  | `false` | Remove unused dependencies                 |
| `packages_unattended_upgrades_enabled` | `false` | Configure automatic security updates       |
| `packages_apt_proxy_enabled`           | `false` | Configure an APT proxy                     |
| `packages_keys_force_update`           | `false` | Force re-download of all keyring files     |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/packages_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. GPG key import shell tasks use `creates:` (skipped when the keyring exists), and cache probes are `changed_when: false`, so no system changes occur in check mode.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
