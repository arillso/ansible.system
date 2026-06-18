# Ansible Role: ansible

Configures Ansible automation with systemd timers for self-managing infrastructure.

## Features

- **Ansible Pull Mode**: Repository-first configuration with git integration
- **Local Playbook Mode**: Execute local playbooks on schedule
- **Systemd Timers**: Flexible scheduling with systemd calendar syntax
- **Self-Healing**: Automatic configuration drift correction
- **Logging**: Comprehensive logging with rotation

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/ansible_role.html](https://guide.arillso.io/collections/arillso/system/ansible_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.ansible
        vars:
            ansible_mode: pull
            ansible_pull_url: https://github.com/myorg/infra.git
```

## Variables

| Variable                       | Default      | Description                                   |
| ------------------------------ | ------------ | --------------------------------------------- |
| `ansible_mode`                 | `"pull"`     | Execution mode (`pull` or local playbook)     |
| `ansible_repo`                 | `""`         | Git repository URL for pull mode              |
| `ansible_branch`               | `"main"`     | Git branch to check out                       |
| `ansible_playbook`             | `"site.yml"` | Playbook to run                               |
| `ansible_schedule`             | `"*:0/15"`   | systemd timer `OnCalendar` schedule           |
| `ansible_random_delay`         | `300`        | Randomized timer delay in seconds             |
| `ansible_install_method`       | `"pipx"`     | How Ansible is installed                      |
| `ansible_pipx_inject_packages` | `[]`         | Extra Python deps injected into the pipx venv |
| `ansible_otel_enabled`         | `false`      | Enable OpenTelemetry export                   |
| `ansible_install_collections`  | `true`       | Install collections from requirements file    |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/ansible_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fully supported; package install, file, and systemd timer tasks use idempotent modules.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
