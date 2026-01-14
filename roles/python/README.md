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

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
