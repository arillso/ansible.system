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

## Variables

| Variable                             | Default          | Description                              |
| ------------------------------------ | ---------------- | ---------------------------------------- |
| `bitwarden_secrets_version`          | `"1.0.0"`        | `bws` CLI version to install             |
| `bitwarden_secrets_install_path`     | `/usr/local/bin` | Install directory for the binary         |
| `bitwarden_secrets_binary_name`      | `bws`            | Installed binary name                    |
| `bitwarden_secrets_state`            | `present`        | `present` to install, `absent` to remove |
| `bitwarden_secrets_force_install`    | `false`          | Force re-download regardless of version  |
| `bitwarden_secrets_download_timeout` | `120`            | Download timeout in seconds              |
| `bitwarden_secrets_retry_count`      | `3`              | Download retry attempts                  |

See [`defaults/main.yml`](defaults/main.yml) for the complete list and [the guide](https://guide.arillso.io/collections/arillso/system/bitwarden_secrets_role.html) for detailed docs.

## Check Mode

This role is partially `--check` compatible. The installed-version probe (`bws --version`) returns no output in check mode, so the "needs install" decision and download steps cannot be evaluated accurately on a host where the binary is not yet present.

## License

MIT

## Author Information

This role was created by [arillso](https://github.com/arillso).
