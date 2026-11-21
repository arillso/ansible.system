# Ansible Collection: arillso.system

[![CI][ci-badge]][ci-url]
[![Ansible Galaxy][galaxy-badge]][galaxy-url]
[![License: MIT][license-badge]][license-url]

[ci-badge]: https://github.com/arillso/ansible.system/actions/workflows/merge.yml/badge.svg?branch=main
[ci-url]: https://github.com/arillso/ansible.system/actions/workflows/merge.yml
[galaxy-badge]: https://img.shields.io/badge/ansible--galaxy-arillso.system-blue.svg
[galaxy-url]: https://galaxy.ansible.com/ui/repo/published/arillso/system/
[license-badge]: https://img.shields.io/github/license/arillso/ansible.system.svg
[license-url]: LICENSE

Roles and plugins that configure Linux hosts: users and SSH, packages, network,
firewall, logging, systemd, and kernel tuning.

## Quickstart

```bash
ansible-galaxy collection install arillso.system
```

```yaml
---
- name: Configure base system
  hosts: all
  become: true
  roles:
      - arillso.system.packages
      - arillso.system.access
      - arillso.system.firewall
```

To require a minimum version, add it to `requirements.yml`:

```yaml
---
collections:
    - name: arillso.system
      version: ">=2.0.0"
```

Requires `ansible-core >= 2.18`. Galaxy installs the dependencies
`ansible.posix`, `community.general` and `community.crypto`. The TOML filters
need Python 3.11+ on the controller, and `to_toml` / `to_nice_toml` also need
the `tomli-w` package (`pip install tomli-w`).

## Roles

| Role                                         | Purpose                                                           |
| -------------------------------------------- | ----------------------------------------------------------------- |
| [access](roles/access)                       | Users, groups, SSH and sudo                                       |
| [ansible](roles/ansible)                     | Scheduled ansible-pull or ansible-playbook runs via systemd timer |
| [bitwarden_secrets](roles/bitwarden_secrets) | Bitwarden Secrets Manager CLI (`bws`)                             |
| [facts](roles/facts)                         | Extended facts (cloud, container, security)                       |
| [firewall](roles/firewall)                   | nftables rule sets                                                |
| [logging](roles/logging)                     | rsyslog and logrotate                                             |
| [network](roles/network)                     | netplan and systemd-resolved                                      |
| [packages](roles/packages)                   | APT/DNF packages, pins, unattended upgrades                       |
| [python](roles/python)                       | Python, pip and virtualenvs                                       |
| [ready](roles/ready)                         | Waits until a host is reachable and booted                        |
| [shell](roles/shell)                         | Shell environment, SSH banner and MOTD                            |
| [systemd](roles/systemd)                     | Units, services and journald                                      |
| [thermal](roles/thermal)                     | CPU thermal management (Intel)                                    |
| [tuning](roles/tuning)                       | CPU, IO, network, swap and sysctl tuning                          |
| [zram](roles/zram)                           | Compressed RAM swap via zram-tools                                |

## Plugins

| Plugin                  | Type   | Purpose                                    |
| ----------------------- | ------ | ------------------------------------------ |
| `apt_update_info`       | module | List upgradable APT packages               |
| `reboot_info`           | module | Report whether the host needs a reboot     |
| `environment_files`     | lookup | Curate a file list from patterns           |
| `github_latest_release` | lookup | Latest release tag of a public GitHub repo |
| `from_toml`             | filter | TOML string to dictionary                  |
| `to_toml`               | filter | Variable to TOML string                    |
| `to_nice_toml`          | filter | Variable to formatted TOML string          |
| `to_nftables_hierarchy` | filter | Merge hierarchical firewall configs        |
| `to_nftables_rule`      | filter | Rule dictionary to nftables syntax         |
| `to_nftables_ports`     | filter | Port list to nftables port syntax          |

```yaml
- name: Check for pending reboot
  arillso.system.reboot_info:
  register: reboot

- name: Reboot when required
  ansible.builtin.reboot:
  when: reboot.reboot
```

## Configuration

Each role documents its variables in `meta/argument_specs.yml` and its own
`README.md`; Ansible validates role arguments against the spec at runtime.
Rendered documentation: [guide.arillso.io][docs].

[docs]: https://guide.arillso.io/collections/arillso/system/

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, tests and the release process,
and [tests/README.md](tests/README.md) for the test layers. Changes are listed in
[CHANGELOG.md](CHANGELOG.md).

## License

MIT, see [LICENSE](LICENSE).
