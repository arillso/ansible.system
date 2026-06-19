# Ansible Role: python

Manages Python packages via pip with support for virtualenv and requirements files.

## Features

- **Pip Package Management**: Install packages system-wide or in virtualenvs
- **Requirements Files**: Support for requirements.txt installation
- **Virtualenv Support**: Create and manage virtual environments
- **Version Control**: Install specific package versions
- **Multi-Entry-Point**: Flexible task organization

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/python_role.html](https://guide.arillso.io/collections/arillso/system/python_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.python
        vars:
            python_packages:
                - name: flask
                  virtualenv: /opt/webapp/venv
```

## Variables

| Variable                    | Default                                | Description                                          |
| --------------------------- | -------------------------------------- | ---------------------------------------------------- |
| `python_pip_enabled`        | `true`                                 | Manage pip-installed packages                        |
| `python_virtualenv_enabled` | `true`                                 | Enable virtualenv-based installs                     |
| `python_packages`           | `[]`                                   | Python packages to manage (list of dicts)            |
| `python_pip_executable`     | `pip3`                                 | pip executable to use                                |
| `python_upgrade_pip`        | `false`                                | Upgrade pip itself                                   |
| `python_virtualenv_command` | `python3 -m venv`                      | Command used to create virtualenvs                   |
| `python_install_packages`   | `true`                                 | Install system Python packages                       |
| `python_system_packages`    | `[python3, python3-pip, python3-venv]` | Distro Python packages (RedHat omits `python3-venv`) |
| `python_requirements_files` | `[]`                                   | requirements.txt files to install                    |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/python_role.html) for detailed docs.

## Check Mode

This role supports `--check` mode. Fully supported; package, pip, and venv operations run through idempotent modules.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
