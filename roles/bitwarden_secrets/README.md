# Ansible Role: bitwarden_secrets

Installs the Bitwarden Secrets Manager CLI (`bws`) for secret management.

## Features

- **Binary Installation**: Downloads and installs the `bws` CLI tool
- **Version Management**: Install specific versions or latest
- **Multi-Architecture**: Supports x86_64, aarch64, armv7l
- **Idempotent**: Only downloads if version doesn't match
- **Uninstall Support**: Clean removal when needed

## Documentation

For detailed documentation including all variables, examples, and usage instructions, see:

**[https://guide.arillso.io/collections/arillso/system/bitwarden_secrets_role.html](https://guide.arillso.io/collections/arillso/system/bitwarden_secrets_role.html)**

## Quick Start

```yaml
- hosts: servers
  roles:
      - role: arillso.system.bitwarden_secrets
        vars:
            bitwarden_secrets_version: "1.0.0"
```

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
